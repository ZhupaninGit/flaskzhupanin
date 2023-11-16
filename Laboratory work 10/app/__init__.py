from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

from config import config

def create_app(config_class=config["dev"]):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.main import bp as main
    app.register_blueprint(main)
    from app.todo import bp as todo
    app.register_blueprint(todo,url_prefix="/todo/")
    from app.auth import bp as auth
    app.register_blueprint(auth)
    from app.feedback import bp as feedback
    app.register_blueprint(feedback,url_prefix="/feedbacks")
    from app.cookies import bp as cookies
    app.register_blueprint(cookies,url_prefix="/cookies")

    return app