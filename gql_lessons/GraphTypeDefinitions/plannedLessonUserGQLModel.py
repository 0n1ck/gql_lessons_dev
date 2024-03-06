from typing import List, Union, Annotated, Optional
import strawberry as strawberryA
import datetime
import typing
import uuid
import strawberry
from gql_lessons.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

from ._GraphResolvers import (
    resolve_id,

    resolve_created,
    resolve_lastchange,
    resolve_changedby,
    resolve_createdby,
    
    createRootResolver_by_id,
)

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel",strawberry.lazy(".plannedLessonGQLModel")]


@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a planned lesson user"""
)
class PlannedLessonUserGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).userplan_lessons

    id = resolve_id

    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    
    @strawberry.field(description="""User, related to a lesson""")
    def users(self) -> Union["UserGQLModel", None]:
        from .externals import UserGQLModel
        return UserGQLModel(id=self.user_id)
    
    @strawberryA.field(description="""Lesson plan type""")
    async def plan_lesson(self, info: strawberryA.types.Info) -> Optional ["PlannedLessonGQLModel"]:
        from .plannedLessonGQLModel import PlannedLessonGQLModel  # Import here to avoid circular dependency
        result = await PlannedLessonGQLModel.resolve_reference(info, self.linkedlesson_id)
        return result
    
###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from contextlib import asynccontextmanager

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class PlannedLessonUserWhereFilter:
    name: str
    type_id: uuid.UUID
    createdby: uuid.UUID

@strawberryA.field(description="""Returns a list of lessons by user""")
async def planned_lesson_user_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PlannedLessonUserWhereFilter] = None
) -> List[PlannedLessonUserGQLModel]:
    loader = getLoadersFromInfo(info).userplan_lessons
    wf = None if where is None else strawberryA.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

planned_lesson_user_by_id = createRootResolver_by_id(PlannedLessonUserGQLModel, description="Returns plan by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional

@strawberryA.input
class PlannedLessonUserInsertGQLModel:
    user_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberryA.input
class PlannedLessonUserUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the user")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    user_id: uuid.UUID
    planlesson_id: uuid.UUID
    
@strawberryA.type(description="Result of a mutation for user type")
class PlannedLessonUserResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the user", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the user type")
    async def user(self, info: strawberryA.types.Info) -> Union[PlannedLessonUserGQLModel, None]:
        result = await PlannedLessonUserGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class PlannedLessonUserDeleteGQLModel:
    user_id: uuid.UUID
    planlesson_id: uuid.UUID
    

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new user.")
async def planned_lesson_user_insert(self, info: strawberryA.types.Info, user: PlannedLessonUserInsertGQLModel) -> PlannedLessonUserResultGQLModel:
    # user = getUserFromInfo(info)
    # user.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).userplan_lessons
    row = await loader.insert(user)
    result = PlannedLessonUserResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Updates the user.",)
async def planned_lesson_user_update(self, info: strawberryA.types.Info, user: PlannedLessonUserUpdateGQLModel) -> PlannedLessonUserResultGQLModel:
    # user = getUserFromInfo(info)
    # user.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).userplan_lessons
    row = await loader.update(user)
    result = PlannedLessonUserResultGQLModel()
    result.msg = "ok"
    result.id = user.id
    result.msg = "ok" if (row is not None) else "fail"
    return result

@strawberry.mutation(description="Deletes the user.")
async def planned_lesson_user_remove(self, info: strawberryA.types.Info, id: uuid.UUID) -> PlannedLessonUserResultGQLModel:
    loader = getLoadersFromInfo(info).userplan_lessons
    row = await loader.delete(id=id)
    result = PlannedLessonUserResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result