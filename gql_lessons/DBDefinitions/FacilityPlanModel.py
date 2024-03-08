import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    ForeignKey,
    Column,
    DateTime,
)
from .UUID import UUIDColumn, UUIDFKey
from .BaseModel import BaseModel

class FacilityPlanModel(BaseModel):
    __tablename__ = "plan_lessons_facilities"

    id = UUIDColumn()
    facility_id = UUIDFKey(nullable=True, comment="Id of planned lesson facility")#Column(ForeignKey("facilities.id"), index=True)
    planlesson_id = Column(ForeignKey("plan_lessons.id"), index=True, comment="Id of planned lesson")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when was planned lesson facility created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when was planned lesson facility last changed")
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)