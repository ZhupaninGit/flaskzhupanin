from flask import Blueprint

bp = Blueprint('feedback', __name__,template_folder="templates/feedback")

from app.feedback import routes