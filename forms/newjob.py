from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class NewJob(FlaskForm):
    team_leader = IntegerField('id капитана', validators=[DataRequired()])
    job = StringField('Описание работы')
    work_size = IntegerField('Объем работы в часах')
    collaborators = StringField('список id участников')
    is_finished = BooleanField('Работа завершена?')
    submit = SubmitField('Применить')
