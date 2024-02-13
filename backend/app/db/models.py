import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext import asyncio as sa_async


class Base(sa_async.AsyncAttrs, orm.DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    # time_entries = orm.relationship("TimeEntry", back_populates="project")


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = sa.Column(sa.Integer, primary_key=True)
    start_time = sa.Column(sa.TIMESTAMP, nullable=False)
    end_time = sa.Column(sa.TIMESTAMP, nullable=True)
    project_id = sa.Column(sa.Integer, sa.ForeignKey("projects.id"))

    # project = orm.relationship("Project", back_populates="time_entries")
