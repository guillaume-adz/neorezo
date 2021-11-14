# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http

from odoo.addons.graphql_base import GraphQLControllerMixin

from ..schema import schema


class NeoRezoController(http.Controller, GraphQLControllerMixin):

    # The GraphiQL route, providing an IDE for developers
    @http.route("/graphiql/neorezo", auth="user")
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
    @http.route("/graphql/neorezo", auth="api_key", csrf=False, save_session=False)
    def graphql(self, **kwargs):
        return self._handle_graphql_request(schema)
