from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length , Email , EqualTo

class changePasswordForm(FlaskForm):
    newpassword = PasswordField('Введіть новий пароль', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=4, max=10)])
    submit = SubmitField("Змінити пароль")

class toDoForm(FlaskForm):
    newtodo = StringField('Введіть нове завдання', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=100)])
    newtododescription = StringField('Введіть опис до завдання', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=255)])
    submit = SubmitField("Додати")

class FeedbackForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    email = StringField('Електронна пошта', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Email("Некоректний формат електронної адреси.")])
    message = TextAreaField('Відгук', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    submit = SubmitField('Надіслати')

class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    email = StringField('Електронна пошта', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Email("Некоректний формат електронної адреси.")])
    password = PasswordField('Пароль', validators=[DataRequired("Це поле обов'язкове до заповнення!"),Length(min=6 , max=255,message="Мінімальна довжина паролю - 6 символів.")])
    confirm_password = PasswordField('Повторіть пароль', validators=[DataRequired("Це поле обов'язкове до заповнення!"), EqualTo("password",message="Паролі не співпадають!")])
    submit = SubmitField('Зареєструватися')

class LoginForm(FlaskForm):
    email = StringField('Електронна пошта', validators=[DataRequired("Це поле обов'язкове до заповнення!"),Email("Некоректний формат електронної адреси.")])
    password = PasswordField('Пароль', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=6, max=255,message="Мінімальна довжина паролю - 6 символів.")])
    remember = BooleanField('Запам\'ятати мене')
    submit = SubmitField("Увійти")