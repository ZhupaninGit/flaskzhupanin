from app.auth import bp
from flask import redirect,render_template,flash,url_for,request
from flask_login import current_user,login_user,login_required,logout_user
from .forms import LoginForm,RegistrationForm,ChangeAccountInfoForm,changePasswordForm
from app.models import User
from app import db
from datetime import datetime
from app import bcrypt
from app.post.photo import delete_photo,save_photo

@bp.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash(f"Ви вже ввійшли в свій аккаунт.", category="successs")
        return redirect(url_for("auth.account"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                flash(f"Успішний вхід! Привіт, {user.username}.", category="successs")
                return redirect(url_for("auth.account"))
        else:
            flash('Помилка! Ім\'я користувача або пароль неправильні.', category="error")
    return render_template('login.html',
                           form=form,
                           active="Увійти",
                           title="Увійти")

@bp.route('/register/',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        flash(f"Ви вже ввійшли в свій аккаунт.", category="successs")
        return redirect(url_for("auth.account"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        newuser = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(newuser)
        db.session.commit()
        flash(f"Користувач {form.username.data} успішно створений!Тепер Ви можете увійти в свій аккаунт.",category="successs")
        return redirect(url_for("auth.login"))
    return render_template('register.html',
                           form=form,
                           active="Реєстрація",
                           title="Реєстрація аккаунта")

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/account/',methods=['POST', 'GET'])
@login_required
def account():
    formChange = ChangeAccountInfoForm()
    if formChange.validate_on_submit():
        if formChange.image.data:
            print(formChange.image.data)
            delete_photo(current_user.image)
            picture_file = save_photo(formChange.image.data)
            current_user.image = picture_file
        current_user.username = formChange.username.data
        current_user.email = formChange.email.data
        current_user.about_me = formChange.about.data
        db.session.commit()
        flash('Успішне оновлення даних користувача.', category='successs')
        return redirect(url_for("auth.account"))
    elif request.method == "GET":
        formChange.username.data = current_user.username
        formChange.email.data = current_user.email
        formChange.about.data = current_user.about_me
    return render_template('account.html', formChange=formChange,title="Account")

@bp.route('/logout/', methods=['POST',"GET"])
@login_required
def logout():
    flash(f"Ви успішно вийшли з власного аккаунту.",category="successs")
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/allusers/', methods=['POST', 'GET'])
def allusers():
    allusers = User.query.all()
    return render_template('allusers.html',
                           users=allusers,
                           title="Всі користувачі")

@bp.route('/changepassword/',methods=["POST","GET"])
@login_required
def changepassword():
    form = changePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.oldpassword.data):
            new_password_hashed = bcrypt.generate_password_hash(form.newpassword.data)
            current_user.password = new_password_hashed
            db.session.commit()
            flash('Пароль успішно змінено', 'successs')
            return redirect(url_for('auth.account'))
        else:
            flash('Старий пароль неправильний.', 'error')
    return render_template('changepassword.html', title='Зміна паролю', form=form)