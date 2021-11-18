import logging

from graphene import Field
from graphene import Int
from graphene import List
from graphene import NonNull
from graphene import String
from graphene.types.objecttype import ObjectTypeOptions
from odoo.addons.graphql_base import OdooObjectType

_logger = logging.getLogger(__name__)


def odoo_resolver(object_type, info, domain=None, **kwargs):
    return info.context["env"][object_type._meta.odoo_model].search(domain, **kwargs)


class OdooOptions(ObjectTypeOptions):

    def __init__(self, *args, **kwargs):
        _logger.error("OPTIONSSSSSSSSSSSSSSS")
        _logger.error(args)
        _logger.error(kwargs)
        self.odool_model = kwargs.get('odoo_model')
        if not self.odool_model:
            _logger.error(f"No odoo model defined for ")
        super().__init__(None)
        _logger.error(self.class_type)


class OdooType(OdooObjectType):

    @classmethod
    def __init_subclass_with_meta__(cls, **meta_options):
        _logger.error("TRACEEEEEEEEEEEEEEEEEEEE")
        _logger.error(meta_options)
        # options = ObjectTypeOptions()
        super().__init_subclass_with_meta__(**meta_options)
        odoo_model = meta_options.get('odoo_model')
        if not odoo_model:
            _logger.error(f"No odoo model defined for {cls._meta.name}")
        setattr(cls._meta, "", odoo_model)


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
        # _logger.error(self._type.__class__._meta.odoo_model)
        _logger.error(self._type._meta.odoo_model)
        domain = [('id' '=', id)]
        return odoo_resolver(self._type, info, domain=domain, **kwargs)
