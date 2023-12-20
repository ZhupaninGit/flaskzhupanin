from app.main import bp
from flask import render_template


my_skills = ["Network Basic", "C++ Basic", r"Dart\Flutter Basic", "Operation System", "Python Basic", "Java Basic"]


@bp.route('/')
def info():
    return render_template("info.html",active="Про нас")

@bp.route('/projects')
def projects():
    return render_template("projects.html",active="Проекти")

@bp.route('/contacts')
def contacts():
    return render_template("contacts.html",active="Контакти")

@bp.route('/skills/')
@bp.route('/skills/<int:id>')
def skills(id=None):
    if id is not None:
        if id >= 0 and id < len(my_skills):
            skills=f"Навичка {id + 1}: {my_skills[id]}"
        else:
            skills="Невірний ідентифікатор навички."
    else:
        skills=my_skills
    return render_template('skills.html', skills=skills,active="Skills",title="Skills")

