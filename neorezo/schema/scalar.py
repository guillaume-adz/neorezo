import logging

from graphene import Field
from graphene import Int
from graphene import List
from graphene import NonNull
from graphene import String
from odoo.addons.graphql_base import OdooObjectType

_logger = logging.getLogger(__name__)


def default_list_resolver(parent, info, domain=None, **kwargs):
    domain = domain or [[]]
    return info.context["env"][parent.meta.odoo_model].search(domain, **kwargs)


class OdooList(List):
    """A graphene List with an Odoo aware default resolver."""

    def __init__(self, of_type: OdooObjectType, resolver=None, **kwargs):
        resolver = resolver or default_list_resolver
        super().__init__(NonNull(of_type), required=True, resolver=default_list_resolver,
                         limit=Int(), offset=Int(), **kwargs)


class OdooRecord(Field):
    """A graphene Field with an Odoo aware default resolver."""

    def __init__(self, of_type: OdooObjectType, resolver=None, **kwargs):
        super().__init__(of_type, resolver=self.record_resolver, id=String(required=True))

    def record_resolver(parent, info, id, **kwargs):
        _logger.info(parent)
        _logger.info(info)
        _logger.info(id)
        _logger.info(kwargs)
        domain = [('id' '=', id)]
        return default_list_resolver(parent, info, domain=domain, **kwargs)
