from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,SelectField,FileField,BooleanField,SelectMultipleField
from wtforms.validators import DataRequired, Length 
from flask_wtf.file import FileAllowed
from app.models import Category,Tag
from flask import current_app

def get_categories():
    with current_app.app_context():
        categoryChoice = [(category.id, category.name) for category in Category.query.all()]
    return categoryChoice
def get_tags():
    with current_app.app_context():
        tagChoice = [(tag.id, tag.name) for tag in Tag.query.all()]
    return tagChoice


class postForm(FlaskForm):
    newpost = StringField('Введіть заголовок до нового посту', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=100)])
    newposttext = TextAreaField('Введіть текст до посту', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    image = FileField('Виберіть зображення',validators=[FileAllowed(["jpg","png","jpeg"],message="Можна завантажувати лише файли з розишренням .jpg,.jpeg,.png")])
    type = SelectField(u'Виберіть тип поста', choices=[('news', 'Новини'), ('events', 'Події'), ('blog', 'Блог'), ('other', 'Інше')])
    category = SelectField(u'Виберіть категорію поста', choices=get_categories)
    tag = SelectMultipleField(u'Виберіть теги поста', choices=get_tags,coerce=int)
    enabled = BooleanField('Зробити пост видимим для всіх')
    submit = SubmitField("Додати")

class changePostForm(FlaskForm):
    newpost = StringField('Введіть заголовок до  посту', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=100)])
    newposttext = TextAreaField('Введіть текст до посту', validators=[DataRequired("Це поле обов'язкове до заповнення!")])
    image = FileField('Виберіть зображення',validators=[FileAllowed(["jpg","png","jpeg"],message="Можна завантажувати лише файли з розишренням .jpg,.jpeg,.png")])
    type = SelectField(u'Виберіть тип поста', choices=[('news', 'Новини'), ('events', 'Події'), ('blog', 'Блог'), ('other', 'Інше')])
    category = SelectField(u'Виберіть категорію поста', choices=get_categories)
    tag = SelectMultipleField(u'Виберіть теги поста', choices=get_tags,coerce=int)
    enabled = BooleanField('Зробити пост видимим для всіх')
    submit = SubmitField("Змінити")

class categoryForm(FlaskForm):
    name = StringField('Введіть назву категорії', validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=50)])
    submit = SubmitField("Додати")

class categoryFormChange(FlaskForm):
    name = StringField("Введіть нову назву категорії",validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=50)])
    submit = SubmitField("Змінити")

class tagForm(FlaskForm):
    name = StringField("Введіть новий тег",validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=50)])
    submit = SubmitField("Додати")

class changeTag(FlaskForm):
    name = StringField("Введіть новий тег",validators=[DataRequired("Це поле обов'язкове до заповнення!"), Length(min=1 , max=50)])
    submit = SubmitField("Змінити")

