import logging
import typing as t

import graphene
from graphene.types.objecttype import ObjectTypeOptions
from .types import OdooObjectType

_logger = logging.getLogger(__name__)

SCALARS = [
    graphene.Boolean,
    graphene.Int,
    graphene.Float,
    graphene.String,
    graphene.ID,
]


class OdooOptions(ObjectTypeOptions):
    """Extends Meta model with Odoo model."""

    def __init__(self, cls, odoo_model):
        super().__init__(cls)
        self.odoo_model = odoo_model


class OdooListType(OdooObjectType):
    """Oddo object type with Meta model extended."""

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

    def __init__(self, of_type: t.Type[OdooListType], resolver=None, **kwargs):
        resolver = resolver or self.record_resolver
        for field_name, field_type in of_type.fields().items():
            name = field_type.name or field_name
            arg = self._from_field_to_arg(field_type.type)
            if arg:
                kwargs[field_name] = arg(name=name)
        super().__init__(of_type, resolver=resolver, limit=graphene.Int(), offset=graphene.Int(), **kwargs)

    def record_resolver(self, parent, info, limit=50, offset=0, **kwargs):
        domain = []
        for field, value in kwargs.items():
            domain.append(self._filter(field, value))
        return info.context["env"][self._of_type.odoo_model()].search(domain, limit=limit, offset=offset)

    def _from_field_to_arg(self, scalar):
        if scalar in SCALARS:
            return scalar
        if isinstance(scalar, graphene.NonNull):
            return self._from_field_to_arg(scalar._of_type)

    def _filter(self, field, value):
        """This funtion may be redefined for specific filtering."""
        return field, '=', value
