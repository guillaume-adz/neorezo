from graphene import ObjectType
from graphene import Schema

# from .invoice import InvoiceMixin
from .tenant import TenantMixin


class Query(ObjectType, TenantMixin):
    ...


schema = Schema(query=Query)
