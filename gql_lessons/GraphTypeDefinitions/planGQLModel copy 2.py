# from typing import List, Union, Annotated, Optional
# import strawberry as strawberryA
# import datetime
# import typing
# import uuid
# import strawberry
# from gql_lessons.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
# from .BaseGQLModel import BaseGQLModel

# from ._GraphResolvers import (
#     resolve_id,

#     resolve_created,
#     resolve_lastchange,
#     resolve_changedby,
#     resolve_createdby,
    
#     createRootResolver_by_id,
# )

# AcSemesterGQLModel = Annotated["AcSemesterGQLModel", strawberry.lazy(".externals")]


# @strawberryA.federation.type(
#     keys=["id"], 
#     description="""Entity representing a plan"""
# )
# class PlanGQLModel(BaseGQLModel):
#     @classmethod
#     def getLoader(cls, info):
#         return getLoadersFromInfo(info).plans

#     id = resolve_id
   

#     created = resolve_created
#     lastchange = resolve_lastchange
#     createdby = resolve_createdby
#     changedby = resolve_changedby
    
#     @strawberry.field(description="""Semester, related to a plan""")
#     def semester(self) -> Union["AcSemesterGQLModel", None]:
#         from .externals import AcSemesterGQLModel
#         return AcSemesterGQLModel(id=self.semester_id)
    
# ##########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
# ##########################################################################################################################

# from contextlib import asynccontextmanager

# from dataclasses import dataclass
# from .utils import createInputs

# @createInputs
# @dataclass
# class PlanWhereFilter:
#     name: str
#     type_id: uuid.UUID
#     createdby: uuid.UUID

# @strawberryA.field(description="""Returns a list of plans""")
# async def plan_page(
#     self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
#     where: Optional[PlanWhereFilter] = None
# ) -> List[PlanGQLModel]:
#     loader = getLoadersFromInfo(info).plans
#     wf = None if where is None else strawberryA.asdict(where)
#     result = await loader.page(skip, limit, where = wf)
#     return result

# plan_by_id = createRootResolver_by_id(PlanGQLModel, description="Returns plan by its id")

# ##########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
# ##########################################################################################################################

# from typing import Optional

# @strawberryA.input
# class PlanInsertGQLModel:
#     name: Optional[str] = strawberryA.field(description="Name of plan", default=None)
#     name_en: Optional[str] = strawberryA.field(description="Name of plan in english", default=None)
#     type_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the lesson type in plan", default=None)
#     semester_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the semester associated with the plan ", default=None)

# @strawberryA.input
# class PlanUpdateGQLModel:
#     lastchange: datetime.datetime = strawberryA.field(description="Time of when was plan last changed", default=None)
#     id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of plan")
#     name: Optional[str] = strawberryA.field(description="Name of plan", default=None)
#     name_en: Optional[str] = strawberryA.field(description="Name of plan in english", default=None)
#     type_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the lesson type in plan", default=None)
#     semester_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the semester associated with the plan ", default=None)
    
# @strawberryA.type
# class PlanResultGQLModel:
#     id: strawberryA.ID = strawberryA.field(default=None, description="primary key value of plan")
#     msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

#     @strawberryA.field(description="""Result of plan operation""")
#     async def plan(self, info: strawberryA.types.Info) -> Optional[PlanGQLModel]:
#         result = await PlanGQLModel.resolve_reference(info, self.id)
#         return result
    
# @strawberryA.input
# class PlanDeleteGQLModel:
#     lastchange: datetime.datetime = strawberryA.field(description="Time of when was plan last changed", default=None)
#     id: uuid.UUID = strawberryA.field(description="primary key (UUID), identifies object of plan", default=None)
#     plan_id: Optional[uuid.UUID] = None

# ##########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
# ##########################################################################################################################

# @strawberryA.mutation(description="Adds a new plan.")
# async def plan_insert(self, info: strawberryA.types.Info, plan: PlanInsertGQLModel) -> PlanResultGQLModel:
#     user = getUserFromInfo(info)
#     plan.createdby = uuid.UUID(user["id"])
#     loader = getLoadersFromInfo(info).plans
#     row = await loader.insert(plan)
#     result = PlanResultGQLModel()
#     result.msg = "ok"
#     result.id = row.id
#     return result

# @strawberryA.mutation(description="Update the plan.",)
# async def plan_update(self, info: strawberryA.types.Info, plan: PlanUpdateGQLModel) -> PlanResultGQLModel:
#     user = getUserFromInfo(info)
#     plan.changedby = uuid.UUID(user["id"])
#     loader = getLoadersFromInfo(info).plans
#     row = await loader.update(plan)
#     result = PlanResultGQLModel()
#     result.msg = "ok"
#     result.id = plan.id
#     result.msg = "ok" if (row is not None) else "fail"
#     return result

# @strawberry.mutation(description="Delete the plan.")
# async def plan_remove(self, info: strawberryA.types.Info, id: uuid.UUID) -> PlanResultGQLModel:
#     loader = getLoadersFromInfo(info).plans
#     row = await loader.delete(id=id)
#     result = PlanResultGQLModel(id=id, msg="ok")
#     result.msg = "fail" if row is None else "ok"
#     return result