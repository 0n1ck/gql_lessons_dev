import strawberry
import uuid

from gql_lessons.utils.Dataloaders import getLoadersFromInfo

# @classmethod
# async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
#     return cls(id=id)
@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID): return cls(id=id)


class BaseEternal:
    id: uuid.UUID = strawberry.federation.field(external=True)

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

@strawberry.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference 

@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

@strawberry.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference   

@strawberry.federation.type(extend=True, keys=["id"])
class AcLessonTypeGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference   

@strawberry.federation.type(extend=True, keys=["id"])
class AcTopicGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference   

@strawberry.federation.type(extend=True, keys=["id"])
class AcSemesterGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference      

@strawberry.federation.type(extend=True, keys=["id"])
class RBACObjectGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

