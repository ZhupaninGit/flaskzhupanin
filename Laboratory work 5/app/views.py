from flask import render_template,request,session,redirect,url_for,make_response,flash
import platform
from datetime import datetime
from app import app
import json
from app.forms import LoginForm


cookies = {}

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
    form = LoginForm()
    if 'username' in session: 
        return redirect(url_for('infos'))
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('E:/3 курс/Python web-programming/Laboratory work 5/app/users.json') as f:
        data = json.load(f)
    json_username = data['username']
    json_password = data['password']
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == json_username and password == json_password:
            session['username'] = username
            flash('Успішний вхід.',"successs")
            return redirect(url_for('infos'))
        else:
            flash('Помилка!Ім\'я користувача або пароль неправильні.',"error")
            
    return render_template('login.html',
                           form=form,
                           active="Login",
                           title="Login",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag)


@app.route('/infos/')
def infos():
    form = LoginForm()
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rcookies = request.cookies
    if 'username' in session:
        username = session['username']
        return render_template('infos.html',
                                username=username,
                                form=form,
                                title="Info",
                                os=os_info,
                                datetime=current_time,
                                user_agent=us_ag,
                                cookies=rcookies,
                                )
    return redirect(url_for('login'))



@app.route('/logout/', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/refresh/', methods=['POST'])
def refreshpage():
    if 'username' in session:
        rcookies = request.cookies
        username = session['username']
        return render_template("infos.html",username=username,cookies=rcookies)


    
@app.route('/add_cookie/', methods=['POST'])
def add_cookie():
    if 'username' in session:
        rcookies = request.cookies
        username = session['username']

        cookie_key = request.form['cookie_key']
        cookie_value = request.form['cookie_value']

        if len(cookie_value) == 0 or len(cookie_key) == 0:
            flash("Кукі не були додані,заповніть всі поля.","error")
            response = make_response(render_template("infos.html",username=username,success="Кукі не були додані,заповніть всі поля.",cookies=rcookies))
        else:
            flash("Кукі успішно додані(натисніть на кнопку нижче для оновлення стану кукі).","successs")
            response = make_response(render_template("infos.html",username=username,cookies=rcookies))
            response.set_cookie(cookie_key,cookie_value)
        return response  
    return redirect(url_for('login'))



@app.route('/deletecookie/<key>',methods=["POST","GET"])
def deletecookie(key=None):
    if 'username' in session:
        if key:
            rcookies = request.cookies
            username = session['username']
            flash("Вибраний кукі успішно видалений.(натисніть на кнопку нижче для оновлення стану кукі).","successs")
            response = make_response(render_template("infos.html",username=username,cookies=rcookies))
            response.delete_cookie(key)
            return response
    return redirect(url_for('login'))


@app.route('/deleteallcookies/',methods=["POST","GET"])
def deleteallcookies():
    if 'username' in session:
        rcookies = request.cookies
        username = session['username']
        flash("Вcі кукі були видалені.(натисніть на кнопку нижче для оновлення стану кукі).","successs")
        response = make_response(render_template("infos.html",username=username,cookies=rcookies))
        cookies = request.cookies
        for key in cookies.keys():
            if key != 'session':
                response.delete_cookie(key)
        return response
    return redirect(url_for('login'))

@app.route('/changepassword/',methods=["POST","GET"])
def changepassword():
    if 'username' in session:
        username = session['username']
        rcookies = request.cookies

        if request.method == 'POST':
            new_password = request.form['new_password']
            if len(new_password) != 0:
                with open('E:/3 курс/Python web-programming/Laboratory work 5/app/users.json', 'r') as file:
                    users = json.load(file)
                users["password"] = new_password
                with open('E:/3 курс/Python web-programming/Laboratory work 5/app/users.json', 'w') as file:
                    json.dump(users, file)
                flash("Пароль було успішно змінено.","successs")    
                return render_template("infos.html",username=username,cookies=rcookies)
            flash("Пароль не було змінено,введіть коректне значення.","error")    
            return render_template('infos.html', username=username,cookies=rcookies)
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


