from flask import render_template,request,session,redirect,url_for,flash
import platform
from datetime import datetime
from app import app
import json
import os
jsonstr = """
{
    "username": "Admin",
    "password": "adminpassword"
}
"""

os_info = platform.platform()

my_skills = ["Network Basic","C++ Basic","Dart\Flutter Basic","Operation System","Python Basic","Java Basic"]

@app.route('/')
def info():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("info.html",
                           active="Про нас",
                           title="About Us",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag)

@app.route('/contacts/')
def contacts():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("contacts.html",
                           active="Контакти",
                           title="Contacts",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag)

@app.route('/projects/')
def projects():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("projects.html",
                           active="Проекти",
                           title="Projects",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag
                           )

@app.route('/login/',methods=['POST','GET'])
def login():
    error = None
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('app/users.json') as f:
        data = json.load(f)
    json_username = data['username']
    json_password = data['password']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['userpass']
        if username == json_username and password == json_password:
            session['username'] = username
            return redirect(url_for('infos'))
        else:
            error = 'Помилка!Ім\'я користувача або пароль неправильні.'
            
    return render_template('login.html',
                           error=error,
                           active="Login",
                           title="Login",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag)


@app.route('/infos/')
def infos():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 'username' in session:
        username = session['username']
        return render_template('infos.html',
                                username=username,
                                title="Info",
                                os=os_info,
                                datetime=current_time,
                                user_agent=us_ag
                                )
    return redirect(url_for('login'))

@app.route('/logout/', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/skills/')
@app.route('/skills/<int:id>')
def skills(id=None):
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if id is not None:
        if id >= 0 and id < len(my_skills):
            skill = my_skills[id]
            return render_template('skills.html', skills=f"Навичка {id + 1}: {skill}",
                           active="Skills",
                           title="Skills",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag)
        else:
            return render_template('skills.html', skills="Невірний ідентифікатор навички.",
                            active="Skills",
                            title="Skills",
                            os=os_info,
                            datetime=current_time,
                            user_agent=us_ag)
    else:
        return render_template('skills.html', skills=my_skills,
                            active="Skills",
                            title="Skills",
                            os=os_info,
                            datetime=current_time,
                            user_agent=us_ag)


