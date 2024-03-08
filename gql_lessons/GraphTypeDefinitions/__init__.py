from typing import List, Union, Optional, Annotated
import strawberry as strawberryA
import typing
import strawberry
import uuid
from contextlib import asynccontextmanager
from gql_lessons.utils.Dataloaders import Loaders 

from .externals import UserGQLModel

def getLoaders(info)-> Loaders:
    context = info.context
    loaders = context["loaders"]
    return loaders


from .externals import AcLessonTypeGQLModel
from .externals import AcSemesterGQLModel
from .externals import AcTopicGQLModel
from .externals import EventGQLModel
from .externals import FacilityGQLModel
from .externals import GroupGQLModel
from .externals import UserGQLModel


from .planGQLModel import PlanGQLModel
from .plannedLessonGQLModel import PlannedLessonGQLModel

from .plannedLessonFacilityGQLModel import PlannedLessonFacilityGQLModel
from .plannedLessonGroupGQLModel import PlannedLessonGroupGQLModel
from .plannedLessonUserGQLModel import PlannedLessonUserGQLModel



@strawberry.type(description="""Type for query root""")
class Query:
    
    from .planGQLModel import (
        plan_by_id,
        plan_page,
    )

    plan_by_id = plan_by_id
    plan_page = plan_page

    from .plannedLessonGQLModel import (
        planned_lesson_by_id,
        planned_lesson_page,
    )

    planned_lesson_by_id = planned_lesson_by_id
    planned_lesson_page = planned_lesson_page

    from .plannedLessonFacilityGQLModel import (
        planned_lesson_facility_by_id,
        planned_lesson_facility_page,
    )

    planned_lesson_facility_by_id = planned_lesson_facility_by_id
    planned_lesson_facility_page = planned_lesson_facility_page

    from .plannedLessonGroupGQLModel import (
        planned_lesson_group_page,
        planned_lesson_group_by_id,
    )
   
    planned_lesson_group_page = planned_lesson_group_page
    planned_lesson_group_by_id = planned_lesson_group_by_id

    from .plannedLessonUserGQLModel import (
        planned_lesson_user_page,
        planned_lesson_user_by_id
    )

    planned_lesson_user_page = planned_lesson_user_page
    planned_lesson_user_by_id = planned_lesson_user_by_id

@strawberry.type(description="""Type for mutation root""")
class Mutation:

    from .planGQLModel import (
    plan_insert,
    plan_update,
    plan_remove,
    )
     
    plan_insert = plan_insert
    plan_update = plan_update
    plan_remove = plan_remove
    
    from .plannedLessonGQLModel import (
        planned_lesson_insert,
        planned_lesson_update,
        planned_lesson_remove,
    )

    planned_lesson_insert = planned_lesson_insert
    planned_lesson_remove = planned_lesson_remove
    planned_lesson_update = planned_lesson_update

    from .plannedLessonFacilityGQLModel import (
        planned_lesson_facility_insert,
        planned_lesson_facility_update,
        planned_lesson_facility_remove,
    )

    planned_lesson_facility_insert = planned_lesson_facility_insert
    planned_lesson_facility_update = planned_lesson_facility_update
    planned_lesson_facility_remove = planned_lesson_facility_remove

    from .plannedLessonGroupGQLModel import (
        planned_lesson_group_insert,
        planned_lesson_group_update,
        planned_lesson_group_remove,
    )

    planned_lesson_group_insert = planned_lesson_group_insert
    planned_lesson_group_update = planned_lesson_group_update
    planned_lesson_group_remove = planned_lesson_group_remove

    from .plannedLessonUserGQLModel import (
        planned_lesson_user_insert,
        planned_lesson_user_update,
        planned_lesson_user_remove
    )

    planned_lesson_user_insert = planned_lesson_user_insert
    planned_lesson_user_update = planned_lesson_user_update
    planned_lesson_user_remove = planned_lesson_user_remove


    

    # planned_lesson_user_insert = planned_lesson_user_insert
    # planned_lesson_user_delete = planned_lesson_user_delete

    # planned_lesson_group_insert = planned_lesson_group_insert
    # planned_lesson_group_delete = planned_lesson_group_delete

    # planned_lesson_facility_insert = planned_lesson_facility_insert
    # planned_lesson_facility_delete = planned_lesson_facility_delete
    

schema = strawberry.federation.Schema(query=Query,
types=(UserGQLModel, PlanGQLModel, PlannedLessonGQLModel,PlannedLessonFacilityGQLModel, PlannedLessonGroupGQLModel,
PlannedLessonUserGQLModel), mutation=Mutation)