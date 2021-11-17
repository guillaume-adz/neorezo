import logging

from graphene import Field
from graphene import Int
from graphene import List
from graphene import NonNull
from graphene import String
from odoo.addons.graphql_base import OdooObjectType

_logger = logging.getLogger(__name__)


def odoo_resolver(parent, info, domain=None, **kwargs):
    return info.context["env"][parent.meta.odoo_model].search(domain, **kwargs)


class OdooList(List):
    """A graphene List with an Odoo aware default resolver."""

    def __init__(self, of_type: OdooObjectType, resolver=None, **kwargs):
        resolver = resolver or self.record_resolver
        super().__init__(NonNull(of_type), required=True, resolver=resolver, limit=Int(), offset=Int(), **kwargs)

    def record_resolver(self, parent, info, **kwargs):
        domain = [[]]
        return odoo_resolver(self._of_type, info, domain=domain, **kwargs)


class OdooRecord(Field):
    """A graphene Field with an Odoo aware default resolver."""

    def __init__(self, of_type: OdooObjectType, resolver=None, **kwargs):
        resolver = resolver or self.record_resolver
        super().__init__(of_type, resolver=resolver, id=String(required=True))

    def record_resolver(self, parent, info, id, **kwargs):
        domain = [('id' '=', id)]
        return odoo_resolver(self._type, info, domain=domain, **kwargs)
