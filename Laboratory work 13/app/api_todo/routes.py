from app.api_todo import api_bp
from app.todo.model import Todo
from flask import jsonify,request
from app import db  

from sqlalchemy.exc import IntegrityError

@api_bp.route("/ping",methods=["GET"])
def ping():
    return jsonify({
        "message":"pong"
    })

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
def delete_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    if not todo:
        return jsonify({"message":f"todo with id {id} not found"}),404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({
        "message":"delete successefully"
    }),200
