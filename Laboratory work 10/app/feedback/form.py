from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email 

class FeedbackForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    email = StringField('Електронна пошта', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Email("Некоректний формат електронної адреси.")])
    message = TextAreaField('Відгук', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    submit = SubmitField('Надіслати')