from graphene import Field
from graphene import Int
from graphene import List
from graphene import NonNull
from graphene import String
from odoo.addons.graphql_base import OdooObjectType


class OdooList(List):
    """A graphene List with an Odoo aware default resolver."""

    def __init__(self, of_type: OdooObjectType, odoo_model: str, **kwargs):
        super().__init__(NonNull(of_type), required=True, resolver=self.default_resolver,
                         limit=Int(), offset=Int(), **kwargs)
        self.odoo_model = odoo_model

    @property
    def of_type(self):
        return self._of_type

    @staticmethod
    def default_resolver(self, info, **kwargs):
        domain = [[]]
        return info.context["env"][self.odoo_model].search(domain, **kwargs)


class OdooRecord(Field):
    """A graphene Field with an Odoo aware default resolver."""

    def __init__(self, list: OdooList, **kwargs):
        super().__init__(list.of_type, resolver=self.default_resolver, id=String(required=True))
        self.list = list

    @staticmethod
    def default_resolver(self, info, id, **kwargs):
        domain = [('id' '=', id)]
        return info.context["env"][self.list.odoo_model].search(domain, **kwargs)
