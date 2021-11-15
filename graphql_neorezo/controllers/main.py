# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging

from odoo import http

from odoo.addons.graphql_base import GraphQLControllerMixin

from ..schema import schema


_logger = logging.getLogger(__name__)


class NeoRezoController(http.Controller, GraphQLControllerMixin):

    # The GraphiQL route, providing an IDE for developers
    @http.route("/graphiql/neorezo", auth="apikey")
    def graphiql(self, **kwargs):
        return self._handle_graphiql_request(schema)

    # Optional monkey patch, needed to accept application/json GraphQL
    # requests. If you only need to accept GET requests or POST
    # with application/x-www-form-urlencoded content,
    # this is not necessary.
    GraphQLControllerMixin.patch_for_json("^/graphql/neorezo/?$")

    # The graphql route, for applications.
    # Note csrf=False: you may want to apply extra security
    # (such as origin restrictions) to this route.
    @http.route("/graphql/neorezo", auth="apikey", csrf=False)
    def graphql(self, **kwargs):
        req = http.request.httprequest
        # We use mimetype here since we don't need the other
        # information provided by content_type
        content_type = req.mimetype
        _logger.info(content_type)
        _logger.info(req.data)
        _logger.info(req.data.decode("utf8"))
        data = req.data.decode("utf8")

        from graphql_server import (
            HttpQueryError,
            default_format_error,
            encode_execution_results,
            json_encode,
            load_json_body,
            run_http_query,
        )
        from functools import partial

        try:
            execution_results, all_params = run_http_query(
                schema,
                req.method.lower(),
                data,
                query_data=req.args,
                batch_enabled=False,
                catch=False,
                context={"env": http.request.env},
            )
            result, status_code = encode_execution_results(
                execution_results,
                is_batch=isinstance(data, list),
                format_error=default_format_error,
                encode=partial(json_encode, pretty=False),
            )
        except Exception as e:
            _logger.info(str(e))

        return self._handle_graphql_request(schema)
