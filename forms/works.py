from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Миссия', validators=[DataRequired()])
    work_size = IntegerField("Время выполнения (часы)", validators=[DataRequired()])
    collaborators = StringField("Помощники")
    submit = SubmitField('Создать')