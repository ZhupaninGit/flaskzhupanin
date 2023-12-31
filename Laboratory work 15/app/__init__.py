from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate(db=db)
marshmallow = Marshmallow()


from config import config

def create_app(config_class=config["dev"]):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)
    marshmallow.init_app(app)
    
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Щоб побачити цю сторінку необхідно авторизуватися!"
    login_manager.login_message_category = "error"


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
    from app.post import bp as post
    app.register_blueprint(post,url_prefix="/post")
    from app.api_todo import api_bp as api
    app.register_blueprint(api)
    from app.api_user import api_user_bp as user_api
    app.register_blueprint(user_api)
    from app.swagger import swaggerui_blueprint as swager_bp
    app.register_blueprint(swager_bp,url_prefix="/swagger")
    return app