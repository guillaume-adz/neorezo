from graphene import Boolean
from graphene import Field
from graphene import ID
from graphene import Int
from graphene import List
from graphene import String

from .scalar import OdooList
from .scalar import OdooRecord
from .scalar import OdooType


class Tenant(OdooType):
    class Meta:
        description = "Tenant defined in ODOO from NeoRezo."
        odoo_model = "res.company"

    id = ID(required=True)
    name = String(required=True)
    tenant_prefix = String(name="prefix", required=True)
    tenant_parent = Field('odoo.addons.neorezo.schema.tenant.Tenant', name="parent", required=True)
    invoices = List(
        Field('odoo.addons.neorezo.schema.invoice.Invoice'),
        refund_only=Boolean(),
        limit=Int(),
        offset=Int(),
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
    tenants = OdooList(Tenant, required=True)
    tenant = OdooRecord(Tenant)
