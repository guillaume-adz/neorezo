from graphene import Boolean
from graphene import Float
from graphene import NonNull
from graphene import String
from odoo.addons.graphql_base import OdooObjectType

from .scalar import OdooList
from .scalar import OdooRecord


class Invoice(OdooObjectType):
    class Meta:
        description = "Invoice defined in ODOO from NeoRezo."

    name = String(required=True)
    move_type = Boolean(required=True)

    customer = String()
    billing_address1 = String(name="address1")
    billing_address2 = String(name="address2")
    billing_company = String(name="company")
    billing_country = String(name="country")
    billing_email = String(name="email")
    billing_first_name = String(name="first_name")
    billing_last_name = String(name="last_name")
    billing_phone = String(name="phone")
    billing_zip = String(name="zip")

    amount_total_signed = Float(name="total_ttc")
    tax_totals_json = String()

    @staticmethod
    def resolve_customer(parent, info):
        return f"{parent.first_name} {parent.last_name}"


class InvoiceMixin:
    invoices = OdooList("account.move", NonNull(Invoice))
    invoice = OdooRecord(Invoice)

    @staticmethod
    def resolve_invoice(root, info, id, **kwargs):
        root.invoices.resolve_id(info, id)
