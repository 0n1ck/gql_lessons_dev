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

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel",strawberry.lazy(".plannedLessonGQLModel")]


@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a planned lesson group"""
)
class PlannedLessonGroupGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).groupplan_lessons

    id = resolve_id
   

    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    
    @strawberry.field(description="""Group, related to a lesson""")
    def groups(self) -> Union["GroupGQLModel", None]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)
    
    @strawberryA.field(description="""Lesson plan type""")
    async def plan_lesson(self, info: strawberryA.types.Info) -> Optional ["PlannedLessonGQLModel"]:
        from .plannedLessonGQLModel import PlannedLessonGQLModel  # Import here to avoid circular dependency
        result = await PlannedLessonGQLModel.resolve_reference(info, self.planlesson_id)
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
class PlannedLessonGroupWhereFilter:
    name: str
    type_id: uuid.UUID
    createdby: uuid.UUID

@strawberryA.field(description="""Returns a list of planned lesson group""")
async def planned_lesson_group_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PlannedLessonGroupWhereFilter] = None
) -> List[PlannedLessonGroupGQLModel]:
    loader = getLoadersFromInfo(info).groupplan_lessons
    wf = None if where is None else strawberryA.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

planned_lesson_group_by_id = createRootResolver_by_id(PlannedLessonGroupGQLModel, description="Returns planned lesson group by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional

@strawberryA.input
class PlannedLessonGroupInsertGQLModel:
    id: Optional[uuid.UUID]
    group_id: uuid.UUID
    planlesson_id: uuid.UUID

@strawberryA.input
class PlannedLessonGroupUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="Primary key UUID")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    group_id: uuid.UUID = strawberryA.field(description="Id of group")
    planlesson_id: uuid.UUID = strawberryA.field(description="Id of planned lesson")
    
@strawberryA.type(description="Result of a mutation for group type")
class PlannedLessonGroupResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the group", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the group type")
    async def group(self, info: strawberryA.types.Info) -> Union[PlannedLessonGroupGQLModel, None]:
        result = await PlannedLessonGroupGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class PlannedLessonGroupDeleteGQLModel:
    group_id: uuid.UUID = strawberryA.field(description="Id of group")
    planlesson_id: uuid.UUID = strawberryA.field(description="Id of planned lesson")
    

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new group to groupplan_lesson .")
async def planned_lesson_group_insert(self, info: strawberryA.types.Info, group: PlannedLessonGroupInsertGQLModel) -> PlannedLessonGroupResultGQLModel:
    # user = getUserFromInfo(info)
    # group.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).groupplan_lessons
    row = await loader.insert(group)
    result = PlannedLessonGroupResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Updates the group.",)
async def planned_lesson_group_update(self, info: strawberryA.types.Info, group: PlannedLessonGroupUpdateGQLModel) -> PlannedLessonGroupResultGQLModel:
    # user = getUserFromInfo(info)
    # group.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).groupplan_lessons
    row = await loader.update(group)
    result = PlannedLessonGroupResultGQLModel()
    result.msg = "ok"
    result.id = group.id
    result.msg = "ok" if (row is not None) else "fail"
    return result

@strawberry.mutation(description="Deletes the group.")
async def planned_lesson_group_remove(self, info: strawberryA.types.Info, id: uuid.UUID) -> PlannedLessonGroupResultGQLModel:
    loader = getLoadersFromInfo(info).groupplan_lessons
    row = await loader.delete(id=id)
    result = PlannedLessonGroupResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result