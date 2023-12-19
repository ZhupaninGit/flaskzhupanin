from app.api_todo import api_bp
from app.todo.model import Todo
from flask import jsonify,request,current_app
from app import db,bcrypt
from app.models import User
from flask_httpauth import HTTPBasicAuth
import jwt
import datetime
basicAuth = HTTPBasicAuth()

from sqlalchemy.exc import IntegrityError

from flask import g
from functools import wraps

@basicAuth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return True
    return False

@basicAuth.error_handler
def unauthorized():
    return jsonify({"message":"Username or password incorrect!"})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)
    return decorated

def generate_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm='HS256')
        return token
    except Exception as e:
        return e
    
@api_bp.route('/login', methods=['POST'])
@basicAuth.login_required
def login():
    username = basicAuth.username()
    user = User.query.filter_by(username=username).first()

    token = generate_token(user.id)
    return jsonify({'token': token})

@api_bp.route("/todos",methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    todos_list = []
    for todo in todos:
        item = dict(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            complete = todo.complete
        )
        todos_list.append(item)
    return jsonify(todos_list)


@api_bp.route("/todos",methods=["POST"])
@token_required
def post_todos():
    new_data = request.get_json()

    if not new_data:
        return jsonify({"message":"no input data provided"}),400
    
    if not new_data.get("title") or not new_data.get("description"):
        return jsonify({"message":"no keys"}),422


    todo = Todo(title=new_data.get("title"),description=new_data.get("description"))
    
    db.session.add(todo)
    db.session.commit()

    new_todo = Todo.query.filter_by(id=todo.id).first()

    return jsonify({
        "message":"todo created",
        "id":new_todo.id,
        "title":new_todo.title,
        "description":new_todo.description,
    }),201


@api_bp.route("/todos/<int:id>",methods=["GET"])
def get_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({"message":f"todo with id {id} not found"}),404

    return jsonify({
        "id":todo.id,
        "title":todo.title,
        "description":todo.description,
    }),200

@api_bp.route("/todos/<int:id>",methods=["PUT"])
@token_required
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()

    if not todo:
        return jsonify({"message":f"todo with id {id} not found"}),404

    new_data = request.get_json()

    if not new_data:
        return jsonify({"message":"no input data provided"}),400
    
    if new_data.get("title"):
        todo.title = new_data.get("title")

    if new_data.get("description"):
        todo.description = new_data.get("description")
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message":"unexpected data"}),422

    if not new_data.get("title") or not new_data.get("description"):
        return jsonify({"message":"no keys"}),422

    return jsonify({
        "message":"todo was updated"
    }),200


@api_bp.route("/todos/<int:id>",methods=["DELETE"])
@token_required
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    if not todo:
        return jsonify({"message":f"todo with id {id} not found"}),404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({
        "message":"delete successefully"
    }),200
