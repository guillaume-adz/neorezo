from graphene import ObjectType
from graphene import Schema

from .invoice import InvoiceMixin
from .tenant import TenantMixin


class Query(ObjectType, TenantMixin, InvoiceMixin):
    ...


schema = Schema(query=Query, auto_camelcase=False)
