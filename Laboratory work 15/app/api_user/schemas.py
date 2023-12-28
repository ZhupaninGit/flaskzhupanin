from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from app.models import User
from app import marshmallow

class UserSchema(marshmallow.Schema):
    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=4),
            validate.Regexp(
                r'^[A-Za-z][A-Za-z0-9_. ]*$',
                error="Username can only contain letters, numbers, dots, or underscores.",
            ),
        ],
    )
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
    )

    @validates_schema
    def validate_username(self, data, **kwargs):
        existing_user = User.query.filter_by(username=data.get('username')).first()
        if existing_user:
            raise ValidationError('This username is already taken.')

    @validates_schema
    def validate_email(self, data, **kwargs):
        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            raise ValidationError('This email address is already taken.')

class UserPutSchema(marshmallow.Schema):
    username = fields.String(
        validate=[
            validate.Length(min=4),
            validate.Regexp(
                r'^[A-Za-z][A-Za-z0-9_. ]*$',
                error="Username can only contain letters, numbers, dots, or underscores.",
            ),
        ],
    )
    email = fields.Email()


    @validates_schema
    def validate_username(self, data, **kwargs):
        existing_user = User.query.filter_by(username=data.get('username')).first()
        if existing_user:
            raise ValidationError('This username is already taken.')

    @validates_schema
    def validate_email(self, data, **kwargs):
        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            raise ValidationError('This email address is already taken.')