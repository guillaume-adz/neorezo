import logging

from graphene import Boolean
from graphene import Float
from graphene import String

from .scalar import OdooList
from .scalar import OdooRecord
from .scalar import OdooType

_logger = logging.getLogger(__name__)


class Invoice(OdooType):
    class Meta:
        description = "Invoice defined in ODOO from NeoRezo."
        odoo_model = "account.move"

    name = String(name="ref", required=True)
    internal_name = String(name="name", required=True)
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
    invoices = OdooList(Invoice)
    invoice = OdooRecord(Invoice)
