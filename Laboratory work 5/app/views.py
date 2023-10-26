from flask import render_template,request,session,redirect,url_for,make_response,flash
import platform
from datetime import datetime
from app import app
import json
from app.forms import LoginForm,changePasswordForm
from os.path import join,dirname,realpath

jsonPath = join(dirname(realpath(__file__)), 'users.json')


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

    return render_template("contacts.html",
                           active="Контакти",
                           title="Contacts")

@app.route('/projects/')
def projects():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("projects.html",
                           active="Проекти",
                           title="Projects")

@app.route('/login/',methods=['POST','GET'])
def login():
    form = LoginForm()
    if 'username' in session: 
        return redirect(url_for('infos'))

    with open(jsonPath) as f:
        data = json.load(f)
    try:
        json_username = data['username']
        json_password = data['password']
    except:
        flash("Помилка отримання даних користувачів,спробуйте ще раз!","error")
        return redirect(url_for("login"))
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == json_username and password == json_password:
            if form.remember.data:
                session['username'] = username
                flash('Успішний вхід.',"successs")
                return redirect(url_for('infos'))
            else:
                flash('Успішні дані для входу,проте сесію користувача створено не було (виберіть "Запам\'ятати мене" для створення сесії).',"successs")
                return redirect(url_for("info"))
        else:
            flash('Помилка!Ім\'я користувача або пароль неправильні.',"error")
    return render_template('login.html',
                           form=form,
                           active="Login",
                           title="Login")


@app.route('/infos/')
def infos():
    form = LoginForm()
    changePassword = changePasswordForm()
    rcookies = request.cookies
    if 'username' in session:
        username = session['username']
        return render_template('infos.html',
                                username=username,
                                form=form,
                                changePasswordForm = changePassword,
                                title="Info",
                                cookies=rcookies)
    return redirect(url_for('login'))



@app.route('/logout/', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

    
@app.route('/add_cookie/', methods=['POST'])
def add_cookie():
    if 'username' in session:
        cookie_key = request.form['cookie_key']
        cookie_value = request.form['cookie_value']

        if len(cookie_value) == 0 or len(cookie_key) == 0:
            flash("Кукі не були додані,заповніть всі поля.","error")
            response = make_response(redirect(url_for('infos')))
        else:
            flash("Кукі успішно додані.","successs")
            response = make_response(redirect(url_for('infos')))
            response.set_cookie(cookie_key,cookie_value)
        return response  
    return redirect(url_for('login'))



@app.route('/deletecookie/<key>',methods=["POST","GET"])
def deletecookie(key=None):
    if 'username' in session:
        if key:
            flash("Вибраний кукі успішно видалений.","successs")
            response = make_response(redirect(url_for('infos')))
            response.delete_cookie(key)
            return response
    return redirect(url_for('login'))


@app.route('/deleteallcookies/',methods=["POST","GET"])
def deleteallcookies():
    if 'username' in session:
        flash("Вcі кукі були видалені.","successs")
        response = make_response(redirect(url_for('infos')))
        cookies = request.cookies
        for key in cookies.keys():
            if key != 'session':
                response.delete_cookie(key)
        return response
    return redirect(url_for('login'))

@app.route('/changepassword/',methods=["POST","GET"])
def changepassword():
    form = LoginForm()
    rcookies = request.cookies
    changePassword = changePasswordForm()
    if 'username' in session:
        username = session['username']
        if changePassword.validate_on_submit():
            new_password = changePassword.newpassword.data
            print(new_password)
            if len(new_password) < 3 and len(new_password) > 10:
                flash("Пароль не було змінено.","error")    
                return redirect(url_for('infos'))
            else:
                with open(jsonPath, 'r') as file:
                    users = json.load(file)
                users["password"] = new_password
                with open(jsonPath, 'w') as file:
                    json.dump(users, file)
                flash("Пароль було успішно змінено.","successs")    
                return redirect(url_for('infos'))
        return render_template('infos.html',
                                username=username,
                                form=form,
                                changePasswordForm = changePassword,
                                title="Info",
                                cookies=rcookies)




@app.route('/skills/')
@app.route('/skills/<int:id>')
def skills(id=None):
    if id is not None:
        if id >= 0 and id < len(my_skills):
            skill = my_skills[id]
            return render_template('skills.html', skills=f"Навичка {id + 1}: {skill}",
                           active="Skills",
                           title="Skills")
        else:
            return render_template('skills.html', skills="Невірний ідентифікатор навички.",
                            active="Skills",
                            title="Skills")
    else:
        return render_template('skills.html', skills=my_skills,
                            active="Skills",
                            title="Skills")


