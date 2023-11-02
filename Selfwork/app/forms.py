from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length , Email

class LoginForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    password = PasswordField('Пароль', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=4, max=10)])
    remember = BooleanField('Запам\'ятати мене')
    submit = SubmitField("Увійти")

class changePasswordForm(FlaskForm):
    newpassword = PasswordField('Введіть новий пароль', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=4, max=10)])
    submit = SubmitField("Змінити пароль")

class toDoForm(FlaskForm):
    newtodo = StringField('Введіть нове завдання', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=100)])
    newtododescription = StringField('Введіть опис до завдання', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=255)])
    submit = SubmitField("Додати")

class FeedbackForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    email = StringField('Електронна пошта', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Email("Некоректний формат адреси.")])
    message = TextAreaField('Відгук', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    submit = SubmitField('Надіслати')
