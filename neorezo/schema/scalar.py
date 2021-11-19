import logging
import typing as t

from graphene import Boolean
from graphene import Int
from graphene import String
from graphene import List
from graphene.types.argument import to_arguments
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
    def fields(cls):
        return cls._meta.fields

    @classmethod
    def odoo_model(cls):
        return cls._meta.odoo_model


class OdooList(List):
    """A graphene List with an Odoo aware default resolver."""

    def __init__(self, of_type: t.Type[OdooType], resolver=None, **kwargs):
        resolver = resolver or self.record_resolver
        _logger.error("INITTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        for field_name, field_type in of_type.fields().items():
            _logger.error(field_name)
            _logger.error(field_type)
            if field_type is Boolean or field_type is Int or field_type is String:
                _logger.error(f"{field_name} ADDED")
                kwargs[field_name] = to_arguments(field_type)
        super().__init__(of_type, resolver=resolver, limit=Int(), offset=Int(), **kwargs)

    def record_resolver(self, parent, info, limit=50, offset=0, **kwargs):
        domain = []
        for field, value in kwargs.items():
            _logger.error("RESSSSSSSSSSSSSSSSOLVE")
            _logger.error(field)
            _logger.error(value)
            domain.append((field, '=', value))
        return info.context["env"][self._of_type.odoo_model()].search(domain, limit=limit, offset=offset)
