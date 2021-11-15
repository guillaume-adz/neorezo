# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# disable undefined variable error, which erroneously triggers
# on forward declarations of classes in lambdas
# pylint: disable=E0602

import graphene

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.graphql_base import OdooObjectType


class Tenant(OdooObjectType):
    name = graphene.String(required=True)
    tenant_prefix = graphene.String(required=True)


class TenantMixin:
    tenants = graphene.List(
        graphene.NonNull(Tenant),
        required=True,
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    @staticmethod
    def resolve_tenants(root, info, limit=None, offset=None):
        domain = []
        return info.context["env"]["res.company"].search(
            domain, limit=limit, offset=offset
        )

