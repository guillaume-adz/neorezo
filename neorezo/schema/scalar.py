import logging
import typing as t

from graphene import Field
from graphene import Int
from graphene import List
from graphene import String
from graphene.types.objecttype import ObjectTypeOptions
from odoo.addons.graphql_base import OdooObjectType

_logger = logging.getLogger(__name__)


class OdooOptions(ObjectTypeOptions):

    def __init__(self, cls, odoo_model):
        super().__init__(cls)
        self.odoo_model = odoo_model


class OdooType(OdooObjectType):

    @classmethod
    def __init_subclass_with_meta__(cls, **meta_options):
        odoo_model = meta_options.pop('odoo_model', None)
        if not odoo_model:
            raise TypeError(f"No odoo model defined among meta options: {meta_options}")
        meta = OdooOptions(cls, odoo_model)
        super().__init_subclass_with_meta__(_meta=meta, **meta_options)

    @classmethod
    def odoo_model(cls):
        return cls._meta.odoo_model


def odoo_resolver(object_type: OdooType, info, domain=None, **kwargs):
    return info.context["env"][object_type.odoo_model()].search(domain, **kwargs)


class OdooList(List):
    """A graphene List with an Odoo aware default resolver."""

    def __init__(self, of_type: t.Type[OdooType], resolver=None, **kwargs):
        resolver = resolver or self.record_resolver
        super().__init__(of_type, resolver=resolver, limit=Int(), offset=Int(), **kwargs)

    def record_resolver(self, parent, info, limit=50, offset=0, **kwargs):
        domain = []
        return odoo_resolver(self._of_type, info, domain=domain, limit=limit, offset=offset, **kwargs)


class OdooRecord(Field):
    """A graphene Field with an Odoo aware default resolver."""

    def __init__(self, of_type: t.Type[OdooType], resolver=None, **kwargs):
        resolver = resolver or self.record_resolver
        super().__init__(of_type, resolver=resolver, id=String(required=True))

    def record_resolver(self, parent, info, id, **kwargs):
        domain = [('id', '=', id)]
        return odoo_resolver(self._type, info, domain=domain, **kwargs)
