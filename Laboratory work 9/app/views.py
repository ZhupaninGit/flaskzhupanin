from flask import render_template,request,session,redirect,url_for,make_response,flash
import platform
from datetime import datetime
from app import app,db,bcrypt,login_manager
from app.forms import LoginForm,changePasswordForm,toDoForm,FeedbackForm,RegistrationForm,ChangeAccountInfoForm
from app.models import User,Todo,Feedback

from flask_migrate import Migrate
from flask_login import login_user,login_required,logout_user,current_user

import os,secrets
from PIL import Image

def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,"static/profile_pics",picture_fn)

    image = Image.open(form_picture)
    image.thumbnail((500,500))
    image.save(picture_path)

    return picture_fn

migrate = Migrate(app, db)

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
                           title="Контакти")

@app.route('/projects/')
def projects():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("projects.html",
                           active="Проекти",
                           title="Projects")

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash(f"Ви вже ввійшли в свій аккаунт.", category="successs")
        return redirect(url_for("account"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                flash(f"Успішний вхід! Привіт, {user.username}.", category="successs")
                return redirect(url_for("account"))
        else:
            flash('Помилка! Ім\'я користувача або пароль неправильні.', category="error")
    return render_template('login.html',
                           form=form,
                           active="Увійти",
                           title="Увійти")

@app.route('/allusers/', methods=['POST', 'GET'])
def allusers():
    allusers = User.query.all()
    return render_template('allusers.html',
                           users=allusers,
                           title="Всі користувачі")

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/account/',methods=['POST', 'GET'])
@login_required
def account():
    formChange = ChangeAccountInfoForm()
    if formChange.validate_on_submit():
        if formChange.image.data:
            picture_file = save_photo(formChange.image.data)
            current_user.image = picture_file
        current_user.username = formChange.username.data
        current_user.email = formChange.email.data
        current_user.about_me = formChange.about.data
        db.session.commit()
        flash('Успішне оновлення даних користувача.', category='successs')

        return redirect(url_for("account"))
    if request.method == "GET":
        formChange.username.data = current_user.username
        formChange.email.data = current_user.email
        formChange.about.data = current_user.about_me
    return render_template('account.html', formChange=formChange)


@app.route('/register/',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        flash(f"Ви вже ввійшли в свій аккаунт.", category="successs")
        return redirect(url_for("account"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        newuser = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(newuser)
        db.session.commit()
        flash(f"Користувач {form.username.data} успішно створений!Тепер Ви можете увійти в свій аккаунт.",category="successs")
        return redirect(url_for("login"))
    return render_template('register.html',
                           form=form,
                           active="Реєстрація",
                           title="Реєстрація аккаунта")


@app.route('/infos/')
@login_required
def infos():
    changePassword = changePasswordForm()
    rcookies = request.cookies
    username = current_user.username
    return render_template('infos.html',
                            username=username,
                            changePasswordForm=changePassword,
                            title="Info",
                            cookies=rcookies)



@app.route('/logout/', methods=['POST',"GET"])
@login_required
def logout():
    flash(f"Ви успішно вийшли з власного аккаунту.",category="successs")
    logout_user()
    return redirect(url_for('login'))


    
@app.route('/add_cookie/', methods=['POST'])
@login_required
def add_cookie():
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
@login_required
def deletecookie(key=None):
    if key:
        flash("Вибраний кукі успішно видалений.","successs")
        response = make_response(redirect(url_for('infos')))
        response.delete_cookie(key)
        return response
    return redirect(url_for('login'))


@app.route('/deleteallcookies/',methods=["POST","GET"])
@login_required
def deleteallcookies():
        flash("Вcі кукі були видалені.","successs")
        response = make_response(redirect(url_for('infos')))
        cookies = request.cookies
        for key in cookies.keys():
            if key != 'session':
                response.delete_cookie(key)
        return response

@app.route('/changepassword/',methods=["POST","GET"])
@login_required
def changepassword():
    form = changePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.oldpassword.data):
            new_password_hashed = bcrypt.generate_password_hash(form.newpassword.data)
            current_user.password = new_password_hashed
            db.session.commit()
            flash('Пароль успішно змінено', 'successs')
            return redirect(url_for('account'))
        else:
            flash('Старий пароль неправильний.', 'error')

    return render_template('changepassword.html', title='Зміна паролю', form=form)


@app.route('/todo/',methods=["GET","POST"])
def todo():
    toDo = toDoForm()
    todo_list = db.session.query(Todo).all()
    return render_template("todo.html",active="ToDo",title="ToDo",toDoForm=toDo,todolist=todo_list)

@app.route("/add_do/",methods=["GET","POST"])
def add_do():
    toDo = toDoForm()
    todo_list = Todo.query.all()
    if toDo.validate_on_submit():
        newTask = Todo(title=toDo.newtodo.data,description=toDo.newtododescription.data,complete=False)
        db.session.add(newTask)
        db.session.commit()
        flash("Завдання було успішно додано.","successs")    
        return redirect(url_for("todo"))
    flash("Завдання не було додано.","error")    
    return render_template('todo.html',
                                active="ToDo",
                                toDoForm = toDo,
                                title="ToDO",
                                todolist=todo_list)


@app.route("/delete_do/<int:todo_id>")
def delete_do(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"Завдання №{todo_id} було успішно видалено.","successs")    
    return redirect(url_for("todo"))

@app.route("/update_do/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    flash(f"Статус завдання №{todo_id} успішно змінено.","successs")    
    return redirect(url_for("todo"))

@app.route('/feedback/',methods=["GET","POST"])
def feedback():
    feedback = FeedbackForm()
    feedback_list = Feedback.query.all()
    return render_template("feedback.html",active="Відгуки",title="Відгуки",form=feedback,feedback_list=feedback_list)

@app.route("/add_feedback/",methods=["GET","POST"])
def add_feedback():
    feedback = FeedbackForm()
    feedback_list = Feedback.query.all()
    if feedback.validate_on_submit():
        newfeedback = Feedback(name=feedback.name.data, email=feedback.email.data, message=feedback.message.data)
        db.session.add(newfeedback)
        db.session.commit()
        flash("Відгук було успішно додано.","successs")    
        return redirect(url_for("feedback"))
    flash("Відгук не було додано.","error")    
    return render_template('feedback.html',
                                active="Відгуки",
                                form = feedback,
                                title="Відгуки",
                                feedback_list=feedback_list)


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


