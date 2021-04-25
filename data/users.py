import datetime
from sqlalchemy import orm
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    jobs = orm.relation("Jobs", back_populates='user')

    def __repr__(self):
        return f'<User> {User.name} {User.email}'

    def check_password(self, password):
        return password == self.hashed_password

    def __init__(self, surname=0, name=0, age=0, position=0, speciality=0, address=0, email=0,
                 hashed_password=0):
        if surname:
            self.surname = surname
        if name:
            self.name = name
        if age:
            self.age = age
        if position:
            self.position = position
        if speciality:
            self.speciality = speciality
        if address:
            self.address = address
        if email:
            self.email = email
        if hashed_password:
            self.hashed_password = hashed_password
