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
    resolve_name,
    resolve_name_en,
    resolve_order,
    resolve_length,
    resolve_startdate,

    resolve_enddate,

    resolve_created,
    resolve_lastchange,
    resolve_changedby,
    resolve_createdby,
    
    createRootResolver_by_id,
)


UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
FacilityGQLModel = Annotated["FacilityGQLModel", strawberry.lazy(".externals")]

EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".externals")]

AcLessonTypeGQLModel = Annotated["AcLessonTypeGQLModel", strawberry.lazy(".externals")]
AcSemesterGQLModel = Annotated["AcSemesterGQLModel", strawberry.lazy(".externals")]
AcTopicGQLModel = Annotated["AcTopicGQLModel", strawberry.lazy(".externals")]

from .planGQLModel import PlanGQLModel



@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a planned lesson"""
)
class PlannedLessonGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).plan_lessons

    id = resolve_id
    name = resolve_name
    order = resolve_order
    length = resolve_length
    startdate = resolve_startdate

    enddate = resolve_enddate

    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby

    

    # @strawberryA.field(description="""Type of acredited lesson""")
    # async def type(self, info: strawberryA.types.Info) -> Optional ["AcLessonTypeGQLModel"]:
    #     from .externals import AcLessonTypeGQLModel  # Import here to avoid circular dependency
    #     result = await AcLessonTypeGQLModel.resolve_reference(info, self.lessontype_id)
    #     return result
    
    # @strawberry.field(description="""Plan, related to a lesson""")
    # def plan(self) -> Union["PlanGQLModel", None]:
    #     from .planGQLModel import PlanGQLModel
    #     return PlanGQLModel(id=self.plan_id)
    
    @strawberryA.field(
        description="""planned lesson linked to (aka master planned lesson)"""
    )
    async def linked_to(
        self, info: strawberryA.types.Info
    ) -> Union["PlannedLessonGQLModel", None]:
        loader = getLoadersFromInfo(info).plan_lessons
        result = None
        if self.linkedlesson_id is not None:
            result = await loader.load(self.linkedlesson_id)
        return result

    @strawberryA.field(
        description="""planned lessons linked with, even trought master, excluding self"""
    )
    async def linked_with(
        self, info: strawberryA.types.Info
    ) -> List["PlannedLessonGQLModel"]:
        loader = getLoadersFromInfo(info).plan_lessons
        result1 = await loader.load(self.id)
        if self.linkedlesson_id is not None:
            result2 = await loader.filter_by(linkedlesson_id=self.id)
            result1 = [result1, *result2]
        return result1

    @strawberryA.field(description="""List of plan lessons""")
    async def plan(
        self, info: strawberryA.types.Info
    ) -> List["PlanGQLModel"]:
        from .planGQLModel import PlanGQLModel
        loader = getLoadersFromInfo(info).plans
        result = await loader.filter_by(plan_id=self.id)
        return result

    @strawberry.field(description="""User, related to a lesson""")
    def users(self) -> Union["UserGQLModel", None]:
        from .externals import UserGQLModel
        return UserGQLModel(id=self.user_id)

    @strawberry.field(description="""Group, related to a lesson""")
    def groups(self) -> Union["GroupGQLModel", None]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)

    @strawberry.field(description="""Facility, related to a lesson""")
    def facilities(self) -> Union["FacilityGQLModel", None]:
        from .externals import FacilityGQLModel
        return FacilityGQLModel(id=self.facility_id)
    
    @strawberry.field(description="""Topic, related to a lesson""")
    def topic(self) -> Union["AcTopicGQLModel", None]:
        from .externals import AcTopicGQLModel
        return AcTopicGQLModel(id=self.topic_id)

    @strawberry.field(description="""Topic, related to a lesson""")
    def type(self) -> Union["AcLessonTypeGQLModel", None]:
        from .externals import AcLessonTypeGQLModel
        return AcLessonTypeGQLModel(id=self.lessontype_id)

    @strawberry.field(description="""Event, related to a lesson""")
    def event(self) -> Union["EventGQLModel", None]:
        from .externals import EventGQLModel
        return EventGQLModel(id=self.event_id)
    
    @strawberry.field(description="""Semester, related to a lesson""")
    def semester(self) -> Union["AcSemesterGQLModel", None]:
        from .externals import AcSemesterGQLModel
        return AcSemesterGQLModel(id=self.semester_id)
    
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
class PlannedLessonsWhereFilter:
    name: str
    lessontype_id: uuid.UUID
    createdby: uuid.UUID

@strawberryA.field(description="""Returns a list of planned lessons""")
async def planned_lesson_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PlannedLessonsWhereFilter] = None
) -> List[PlannedLessonGQLModel]:
    loader = getLoadersFromInfo(info).plan_lessons
    wf = None if where is None else strawberryA.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

planned_lesson_by_id = createRootResolver_by_id(PlannedLessonGQLModel, description="Returns planned lesson by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional

@strawberryA.input
class PlannedLessonInsertGQLModel:
    id: Optional[uuid.UUID]  = strawberryA.field(default=None, description="could be primary key generated by client, UUID is expected")  # Changed to uuid.UUID
    name: str = strawberryA.field(default=None, description="Name of lesson aka 'Introduction'")
    order: Optional[int] = strawberryA.field(default=1, description="order of the item in plan")
    length: Optional[int] = strawberryA.field(default=2, description="how many 45min intervals")
    startdate: Optional[datetime.datetime] = strawberryA.field(default=None, description="proposal of datetime")
    plan_id: uuid.UUID = strawberryA.field(default=None, description="which plan contains this lesson")
    
    linkedlesson_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="id of lesson from other plan which would be teached with")  # Changed to uuid.UUID
    topic_id: Optional[uuid.UUID] = None  # Changed to uuid.UUID
    lessontype_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="aka Consultation, Laboratory, ...")  # Changed to uuid.UUID
    
    semester_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="link to semester (subject) from accreditation")  # Changed to uuid.UUID
    event_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="event defining when this would be teached")  # Changed to uuid.UUID
   
    plan_id: uuid.UUID = strawberryA.field(default=None, description="which plan contains this lesson")  # Changed to uuid.UUID
   
    

@strawberryA.input
class PlannedLessonUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(default=None, description="time stamp")
    id: uuid.UUID = strawberryA.field(default=None, description="primary key value")
    order: Optional[int] = strawberryA.field(default=None, description="Planned lesson order")
    name: Optional[str] = strawberryA.field(default=None, description="Planned lesson name")
    length: Optional[int] = strawberryA.field(default=None, description="Planned lesson length 1 = 45 min")
    startdate: Optional[datetime.datetime] = strawberryA.field(default=None, description="Planned lesson startdate")

    linkedlesson_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="Id of another Lesson linked to a planned lesson")
    topic_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="Id of Topic linked to planned lesson")
    lessontype_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="Id of Type linked to planned lesson")
    semester_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="Id of Semester linked to planned lesson")
    event_id: Optional[uuid.UUID] = strawberryA.field(default=None, description="Id of Event linked to planned lesson")

@strawberryA.type
class PlannedLessonResultGQLModel:
    id: Union[uuid.UUID, None] = strawberryA.field(default=None, description="Primary key UUID of planned lesson")
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="""Result of lesson operation""")
    async def lesson(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel, None]:
        print("lesson", self.id)
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class PlannedLessonDeleteGQLModel:
    lastchange: datetime.datetime = strawberryA.field(description="Lastchange of planned lesson")
    id: uuid.UUID = strawberryA.field(description="Primary key UUID")
    plan_id: Optional[uuid.UUID] = strawberryA.field(description="Id of linked plan to planned lesson")

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a lessons to plan_lessons table.")
async def planned_lesson_insert(self, info: strawberryA.types.Info, lesson: PlannedLessonInsertGQLModel) -> PlannedLessonResultGQLModel:
    # user = getUserFromInfo(info)
    # lesson.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).plan_lessons
    row = await loader.insert(lesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the lesson in plan_lessons table.",)
async def planned_lesson_update(self, info: strawberryA.types.Info, lesson: PlannedLessonUpdateGQLModel) -> PlannedLessonResultGQLModel:
    # user = getUserFromInfo(info)
    # lesson.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).plan_lessons
    row = await loader.update(lesson)
    result = PlannedLessonResultGQLModel()
    result.msg = "ok"
    result.id = lesson.id
    result.msg = "ok" if (row is not None) else "fail"
    return result

@strawberry.mutation(
    description="Deletes the planned lesson from plan_lessons table.")
async def planned_lesson_remove(self, info: strawberryA.types.Info, id: uuid.UUID) -> PlannedLessonResultGQLModel:
    loader = getLoadersFromInfo(info).plan_lessons
    row = await loader.delete(id=id)
    result = PlannedLessonResultGQLModel(id=id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result