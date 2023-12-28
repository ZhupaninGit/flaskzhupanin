from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Length

class toDoForm(FlaskForm):
    newtodo = StringField('Введіть нове завдання', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=100)])
    newtododescription = StringField('Введіть опис до завдання', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=255)])
    submit = SubmitField("Додати")

