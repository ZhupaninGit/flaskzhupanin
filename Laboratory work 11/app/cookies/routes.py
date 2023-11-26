from app.cookies import bp
from flask_login import login_required,current_user
from flask import redirect,request,url_for,make_response,flash,render_template


@bp.route('/infos/')
@login_required
def infos():
    rcookies = request.cookies
    username = current_user.username
    return render_template('infos.html',
                            username=username,
                            title="Info",
                            cookies=rcookies)

@bp.route('/add_cookie/', methods=['POST'])
@login_required
def add_cookie():
    cookie_key = request.form['cookie_key']
    cookie_value = request.form['cookie_value']

    if len(cookie_value) == 0 or len(cookie_key) == 0:
        flash("Кукі не були додані,заповніть всі поля.","error")
        response = make_response(redirect(url_for('cookies.infos')))
    else:
        flash("Кукі успішно додані.","successs")
        response = make_response(redirect(url_for('cookies.infos')))
        response.set_cookie(cookie_key,cookie_value)
        return response  
    return redirect(url_for('cookies.infos'))



@bp.route('/deletecookie/<key>',methods=["POST","GET"])
@login_required
def deletecookie(key=None):
    if key:
        flash("Вибраний кукі успішно видалений.","successs")
        response = make_response(redirect(url_for('cookies.infos')))
        response.delete_cookie(key)
        return response
    return redirect(url_for('cookies.infos'))


@bp.route('/deleteallcookies/',methods=["POST","GET"])
@login_required
def deleteallcookies():
        flash("Вcі кукі були видалені.","successs")
        response = make_response(redirect(url_for('cookies.infos')))
        cookies = request.cookies
        for key in cookies.keys():
            if key != 'session':
                response.delete_cookie(key)
        return response
