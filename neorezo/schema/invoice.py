import logging

import graphene

from .scalar import OdooList
from .scalar import OdooType

_logger = logging.getLogger(__name__)


class Invoice(OdooType):
    class Meta:
        description = "Invoice defined in ODOO from NeoRezo."
        odoo_model = "account.move"

    id = graphene.ID(required=True)
    ref = graphene.String(name="name", required=True)
    name = graphene.String(name="ref", required=True)
    move_type = graphene.Boolean(required=True)

    billing_address1 = graphene.String(name="address1")
    billing_address2 = graphene.String(name="address2")
    billing_company = graphene.String(name="company")
    billing_country = graphene.String(name="country")
    billing_email = graphene.String(name="email")
    billing_first_name = graphene.String(name="first_name")
    billing_last_name = graphene.String(name="last_name")
    billing_phone = graphene.String(name="phone")
    billing_zip = graphene.String(name="zip")

    amount_total_signed = graphene.Float(name="total_ttc")
    tax_totals_json = graphene.String()

    customer = graphene.String()

    @staticmethod
    def resolve_customer(self, info):
        return f"{self.first_name} {self.last_name}"


class InvoiceMixin:
    invoices = OdooList(Invoice)
