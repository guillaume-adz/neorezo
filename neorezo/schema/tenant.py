# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# disable undefined variable error, which erroneously triggers
# on forward declarations of classes in lambdas
# pylint: disable=E0602

import graphene

from odoo.addons.graphql_base import OdooObjectType


class Invoice(OdooObjectType):
    name = graphene.String(required=True)
    move_type = graphene.Boolean(required=True)
    tax_totals_json = graphene.JSONString(required=True)
    amount_total_signed = graphene.Float()


class Tenant(OdooObjectType):
    name = graphene.String(required=True)
    tenant_prefix = graphene.String(required=True)
    invoices = graphene.List(
        graphene.NonNull(Invoice),
        required=True,
        refund_only=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    @staticmethod
    def resolve_invoices(root, info, refund_only=False, limit=None, offset=None):
        domain = [("company_id", "=", root.id), ("ref", "=like", 'CDF%')]
        # if refund_only:
        #     domain.append(("type_name", "=", True))
        return info.context["env"]["account.move"].search(
            domain, limit=limit, offset=offset
        )


class TenantMixin:
    tenants = graphene.List(
        graphene.NonNull(Tenant),
        required=True,
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    invoices = graphene.List(
        graphene.NonNull(Invoice),
        required=True,
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    @staticmethod
    def resolve_tenants(root, info, **kwargs):
        domain = []
        return info.context["env"]["res.company"].search(domain, **kwargs)

    @staticmethod
    def resolve_invoices(root, info, **kwargs):
        domain = []
        return info.context["env"]["account.move"].search(domain, **kwargs)
