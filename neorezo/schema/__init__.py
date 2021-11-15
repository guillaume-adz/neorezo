import graphene

from .tenant import TenantMixin


class Query(graphene.ObjectType, TenantMixin):
    ...


schema = graphene.Schema(query=Query)
