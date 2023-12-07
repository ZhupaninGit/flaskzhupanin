from app.todo import bp
from flask import render_template,redirect,url_for,flash
from .form import toDoForm
from .model import Todo
from app import db

@bp.route('/todo/',methods=["GET","POST"])
def todo():
    toDo = toDoForm()
    todo_list = db.session.query(Todo).all()
    return render_template("todo.html",active="Список справ",title="Список справ",toDoForm=toDo,todolist=todo_list)

@bp.route("/add_do/",methods=["GET","POST"])
def add_do():
    toDo = toDoForm()
    todo_list = Todo.query.all()
    if toDo.validate_on_submit():
        newTask = Todo(title=toDo.newtodo.data,description=toDo.newtododescription.data,complete=False)
        db.session.add(newTask)
        db.session.commit()
        flash("Завдання було успішно додано.","successs")    
        return redirect(url_for("todo.todo"))
    flash("Завдання не було додано.","error")    
    return render_template('todo.html',
                                active="ToDo",
                                toDoForm = toDo,
                                title="ToDO",
                                todolist=todo_list)


@bp.route("/delete_do/<int:todo_id>")
def delete_do(todo_id):
    todo = db.session.get(Todo,todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"Завдання №{todo_id} було успішно видалено.","successs")    
    return redirect(url_for("todo.todo"))

@bp.route("/update_do/<int:todo_id>")
def update(todo_id):
    todo = db.session.get(Todo,todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    flash(f"Статус завдання №{todo_id} успішно змінено.","successs")    
    return redirect(url_for("todo.todo"))