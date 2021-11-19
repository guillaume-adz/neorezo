import graphene

from .scalar import OdooList
from .scalar import OdooType


class Tenant(OdooType):
    class Meta:
        description = "Tenant defined in ODOO from NeoRezo."
        odoo_model = "res.company"

    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    tenant_prefix = graphene.String(name="prefix", required=True)
    tenant_parent = graphene.Field('odoo.addons.neorezo.schema.tenant.Tenant', name="parent", required=True)
    tenant_active = graphene.Boolean(name="actif", required=True)
    invoices = graphene.List(
        graphene.NonNull('odoo.addons.neorezo.schema.invoice.Invoice'),
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
    tenants = OdooList(Tenant, required=True)
