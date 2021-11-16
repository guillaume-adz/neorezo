from graphene import Field
from graphene import Int
from graphene import List
from graphene import String


class OdooList(List):

    def __init__(self, model: str, *args, **kwargs):
        super().__init__(*args, resolver=self.resolve, limit=Int(), offset=Int(), **kwargs)
        self.model = model

    def resolve(self, info, **kwargs):
        domain = [[]]
        return info.context["env"][self.model].search(domain, **kwargs)


class OdooRecord(Field):

    def __init__(self, list: OdooList, **kwargs):
        super().__init__(list.model, resolver=self.resolve, id=String(required=True))
        self.model = list.model

    def resolve(self, info, id, **kwargs):
        domain = [('id' '=', id)]
        return info.context["env"][self.model].search(domain, **kwargs)
