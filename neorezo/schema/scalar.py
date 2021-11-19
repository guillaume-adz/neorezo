import logging
import typing as t

import graphene
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


class OdooList(graphene.List):
    """A graphene List with an Odoo aware default resolver."""

    def __init__(self, of_type: t.Type[OdooType], resolver=None, **kwargs):
        resolver = resolver or self.record_resolver
        _logger.error("INITTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        for field_name, field_type in of_type.fields().items():
            _logger.error(field_type.name or field_name)
            scalar_type = field_type.type
            arg = self.from_field_to_arg(field_type)
            if arg:
                kwargs[field_type.name or field_name] = arg
            # if (scalar_type is graphene.Boolean) or (scalar_type is graphene.Int) or (scalar_type is graphene.String):
            #     _logger.error(f"{field_name} ADDED")
            #     kwargs[field_name] = scalar_type()
            # elif isinstance(scalar_type, graphene.NonNull):
            #     _logger.error(f"{field_name} ADDED2")
            #     scalar_type = scalar_type._of_type
            #     if (scalar_type is graphene.Boolean) or (scalar_type is graphene.Int) or (
            #             scalar_type is graphene.String):
            #         _logger.error(f"{field_name} ADDED3")
            #         kwargs[field_name] = scalar_type()
        _logger.error(kwargs)
        super().__init__(of_type, resolver=resolver, limit=graphene.Int(), offset=graphene.Int(), **kwargs)

    def record_resolver(self, parent, info, limit=50, offset=0, **kwargs):
        domain = []
        for field, value in kwargs.items():
            _logger.error("RESSSSSSSSSSSSSSSSOLVE")
            _logger.error(field)
            _logger.error(value)
            domain.append((field, '=', value))
        return info.context["env"][self._of_type.odoo_model()].search(domain, limit=limit, offset=offset)

    def from_field_to_arg(self, scalar_type):
        if (scalar_type is graphene.Boolean) or (scalar_type is graphene.Int) or (scalar_type is graphene.String):
            return scalar_type()
        if isinstance(scalar_type, graphene.NonNull):
            return self.from_field_to_arg(scalar_type._of_type)
