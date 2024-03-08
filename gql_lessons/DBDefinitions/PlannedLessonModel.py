import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Column,
    DateTime,
)
from .UUID import UUIDColumn, UUIDFKey
from .BaseModel import BaseModel

class PlannedLessonModel(BaseModel):
    """Defines a lesson which is going to be planned in timetable"""

    __tablename__ = "plan_lessons"

    id = UUIDColumn()
    name = Column(String, comment="Name of planned lesson")
    order = Column(Integer, default=lambda:1, comment="Order of planned lesson")
    length = Column(Integer, nullable=True, comment="Length of planned lesson")
    startdate = Column(DateTime, nullable=True, comment="Startdate of planned lesson")
    plan_id = Column(ForeignKey("plans.id"), index=True, nullable=True, comment="Id of planned lesson plan")

    linkedlesson_id = Column(ForeignKey("plan_lessons.id"), index=True, nullable=True, comment="Other lesson linked to planned lesson")
    topic_id = UUIDFKey(nullable=True, comment="Id of topic")#Column(ForeignKey("actopics.id"), index=True, nullable=True)
    lessontype_id = UUIDFKey(nullable=True, comment="Id of lesson type")#Column(ForeignKey("aclessontypes.id"), index=True)

    # neni nadbytecne, topic_id muze byt null, pak je nutne mit semester_id, jedna-li se o akreditovanou vyuku
    semester_id = UUIDFKey(nullable=True, comment="Id of acredited semester")#Column(ForeignKey("acsemesters.id"), index=True, nullable=True)
    event_id = UUIDFKey(nullable=True, comment="Id of event")#Column(ForeignKey("events.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when was planned lesson created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when was planned lesson last changed")
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)