import graphene

# from .invoice import InvoiceMixin
from .tenant import TenantMixin


class Query(graphene.ObjectType, TenantMixin):
    ...


schema = graphene.Schema(query=Query, auto_camelcase=False, )
