from flask import Blueprint

bp = Blueprint('cookies', __name__,template_folder="templates/cookies")

from app.cookies import routes