import datetime
from sqlalchemy import orm
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user = orm.relation('User')

    def __init__(self, id=0, team_leader=0, job=0, work_size=0, collaborators=0, start_date=0, end_date=0,
                 is_finished=0):
        if id:
            self.id = id
        if team_leader:
            self.team_leader = team_leader
        if job:
            self.job = job
        if work_size:
            self.work_size = work_size
        if collaborators:
            self.collaborators = collaborators
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        if is_finished:
            self.is_finished = is_finished
