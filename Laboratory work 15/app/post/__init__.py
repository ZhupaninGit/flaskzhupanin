from flask import Blueprint

bp = Blueprint('post', __name__,template_folder="templates/post")

from app.post import routes