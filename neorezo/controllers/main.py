# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging

from odoo import http
from odoo.addons.graphql_base import GraphQLControllerMixin

from ..schema import schema

_logger = logging.getLogger(__name__)


class NeoRezoController(http.Controller, GraphQLControllerMixin):

    # The GraphiQL route, providing an IDE for developers
    @http.route("/graphiql", auth="apikey")
    def graphiql(self, **kwargs):
        try:
            return self._handle_graphiql_request(schema)
        except Exception as e:
            _logger.info(str(e))

    # Optional monkey patch, needed to accept application/json GraphQL
    # requests. If you only need to accept GET requests or POST
    # with application/x-www-form-urlencoded content,
    # this is not necessary.
    GraphQLControllerMixin.patch_for_json("^/graphql/?$")

    # The graphql route, for applications.
    # Note csrf=False: you may want to apply extra security
    # (such as origin restrictions) to this route.
    @http.route("/graphql", auth="apikey", csrf=False)
    def graphql(self, **kwargs):
        try:
            return self._handle_graphql_request(schema)
        except Exception as e:
            _logger.error("ERRRRRRRRRRRRRRRRRRRRRR")
            _logger.error(str(e))
