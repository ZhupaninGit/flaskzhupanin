from flask import Blueprint
from flask_restful import Api
from app.api_user.routes import UserApi,UsersApi


api_user_bp = Blueprint('api_user_bp', __name__,url_prefix="/api")
api = Api(api_user_bp)

api.add_resource(UserApi,'/user/<int:user_id>')
api.add_resource(UsersApi,'/users')

from app.api_user import routes