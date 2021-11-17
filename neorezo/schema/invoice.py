from graphene import Boolean
from graphene import Float
from graphene import String
from graphene import Field
from odoo.addons.graphql_base import OdooObjectType

from .scalar import OdooList
from .scalar import OdooRecord
import logging
_logger = logging.getLogger(__name__)


class Invoice(OdooObjectType):
    class Meta:
        description = "Invoice defined in ODOO from NeoRezo."
        odoo_model = "account.move"

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

def default_list_resolver(parent, info, domain=None, **kwargs):
    domain = domain or [[]]
    return info.context["env"][parent.meta.odoo_model].search(domain, **kwargs)

class InvoiceMixin:
    invoices = OdooList(Invoice)
    invoice = OdooRecord(Invoice)
    inv = Field(Invoice, resolver=record_resolver, id=String(required=True))

    @staticmethod
    def resolve_invoice(parent, info, id, **kwargs):
        return f"{parent.first_name} {parent.last_name}"

    def record_resolver(self, info, id, **kwargs):
        _logger.info(self)
        _logger.info(info)
        _logger.info(id)
        _logger.info(kwargs)
        domain = [('id' '=', id)]
        return default_list_resolver(self, info, domain=domain, **kwargs)

