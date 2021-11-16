from graphene import Field
from graphene import Int
from graphene import List
from graphene import NonNull
from graphene import String
from odoo.addons.graphql_base import OdooObjectType


def default_list_resolver(parent, info, domain=None, **kwargs):
    domain = domain or [[]]
    return info.context["env"][parent.meta.odoo_model].search(domain, **kwargs)


class OdooList(List):
    """A graphene List with an Odoo aware default resolver."""

    def __init__(self, of_type: OdooObjectType, **kwargs):
        super().__init__(NonNull(of_type), required=True, resolver=default_list_resolver,
                         limit=Int(), offset=Int(), **kwargs)


def record_resolver(parent, info, id, **kwargs):
    domain = [('id' '=', id)]
    return default_list_resolver(parent, info, domain=domain, **kwargs)


class OdooRecord(Field):
    """A graphene Field with an Odoo aware default resolver."""

    def __init__(self, of_type: OdooObjectType, **kwargs):
        super().__init__(of_type, resolver=record_resolver, id=String(required=True))
