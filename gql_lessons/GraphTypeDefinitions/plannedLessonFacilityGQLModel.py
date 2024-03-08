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

FacilityGQLModel = Annotated["FacilityGQLModel", strawberry.lazy(".externals")]
PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel",strawberry.lazy(".plannedLessonGQLModel")]

@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a planned lesson faclity"""
)
class PlannedLessonFacilityGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).facilityplan_lessons

    id = resolve_id
   

    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    
    @strawberry.field(description="""Facility, related to a lesson""")
    def facilities(self) -> Union["FacilityGQLModel", None]:
        from .externals import FacilityGQLModel
        return FacilityGQLModel(id=self.facility_id)
    
    @strawberryA.field(description="""Planned lesson""")
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
class PlannedLessonFacilityWhereFilter:
    name: str
    id: uuid.UUID
    createdby: uuid.UUID

@strawberryA.field(description="""Returns a list of planned lesson facility page""")
async def planned_lesson_facility_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PlannedLessonFacilityWhereFilter] = None
) -> List[PlannedLessonFacilityGQLModel]:
    loader = getLoadersFromInfo(info).facilityplan_lessons
    wf = None if where is None else strawberryA.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

planned_lesson_facility_by_id = createRootResolver_by_id(PlannedLessonFacilityGQLModel, description="Returns planned lesson facility by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional

@strawberryA.input
class PlannedLessonFacilityInsertGQLModel:
    id: Optional[uuid.UUID]
    facility_id: Optional[uuid.UUID] = strawberry.field(description="Id of facility", default=None)
    planlesson_id: Optional[uuid.UUID] = strawberry.field(description="Id of planned lesson", default=None)

@strawberryA.input
class PlannedLessonFacilityUpdateGQLModel:
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key UUID", default=None)
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    facility_id: Optional[uuid.UUID] = strawberry.field(description="Id of facility", default=None)
    planlesson_id: Optional[uuid.UUID] = strawberry.field(description="Id of planned lesson", default=None)
    
@strawberryA.type(description="Result of a mutation for facility type")
class PlannedLessonFacilityResultGQLModel:
    id: uuid.UUID = strawberryA.field(description=" Primary key UUID", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the facility type")
    async def facility(self, info: strawberryA.types.Info) -> Union[PlannedLessonFacilityGQLModel, None]:
        result = await PlannedLessonFacilityGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class PlannedLessonFacilityDeleteGQLModel:
    facility_id: Optional[uuid.UUID] = strawberry.field(description="Id of facility", default=None)
    planlesson_id: Optional[uuid.UUID] = strawberry.field(description="Id of planned lesson", default=None)
    

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new facility to facilityplan_lesson table.")
async def planned_lesson_facility_insert(self, info: strawberryA.types.Info, facility: PlannedLessonFacilityInsertGQLModel) -> PlannedLessonFacilityResultGQLModel:
    # user = getUserFromInfo(info)
    # facility.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).facilityplan_lessons
    row = await loader.insert(facility)
    result = PlannedLessonFacilityResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Updates the facility in facilityplan_lessons table.",)
async def planned_lesson_facility_update(self, info: strawberryA.types.Info, facility: PlannedLessonFacilityUpdateGQLModel) -> PlannedLessonFacilityResultGQLModel:
    # user = getUserFromInfo(info)
    # facility.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).facilityplan_lessons
    row = await loader.update(facility)
    result = PlannedLessonFacilityResultGQLModel()
    result.msg = "ok"
    result.id = facility.id
    result.msg = "ok" if (row is not None) else "fail"
    return result

@strawberry.mutation(description="Deletes the facility from facilityplan_lessons table.")
async def planned_lesson_facility_remove(self, info: strawberryA.types.Info, id: uuid.UUID) -> PlannedLessonFacilityResultGQLModel:
    loader = getLoadersFromInfo(info).facilityplan_lessons
    row = await loader.delete(id=id)
    result = PlannedLessonFacilityResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result