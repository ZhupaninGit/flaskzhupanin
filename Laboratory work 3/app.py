from flask import Flask,render_template
import platform
from datetime import datetime

from flask import request

app = Flask(__name__)
os_info = platform.platform()

my_skills = ["Network Basic","C++ Basic","Dart\Flutter Basic","Operation System","Python Basic","Java Basic"]

@app.route('/')
def info():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("info.html",
                           aboutactive="active",
                           projectsactive="",
                           skillsactive="",
                           contactsactive="",
                           title="About Us",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag)

@app.route('/contacts/')
def contacts():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("contacts.html",
                           aboutactive="",
                           projectsactive="",
                           contactsactive="active",
                           skillsactive="",
                           title="Contacts",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag)

@app.route('/projects/')
def projects():
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template("projects.html",
                           aboutactive="",
                           projectsactive="active",
                           contactsactive="",
                           skillsactive="",
                           title="Projects",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag
                           )

@app.route('/skills/')
@app.route('/skills/<int:id>')
def skills(id=None):
    us_ag = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if id is not None:
        if id >= 0 and id < len(my_skills):
            skill = my_skills[id]
            return render_template('skills.html', skills=f"Навичка {id + 1}: {skill}",aboutactive="",
                           projectsactive="",
                           contactsactive="",
                           skillsactive="active",
                           title="Skills",
                           os=os_info,
                           datetime=current_time,
                           user_agent=us_ag)
        else:
            return render_template('skills.html', skills="Невірний ідентифікатор навички.",aboutactive="",
                           projectsactive="",
                           contactsactive="",
                           skillsactive="active",title="Skills",
                            os=os_info,
                            datetime=current_time,
                            user_agent=us_ag)
    else:
        return render_template('skills.html', skills=my_skills, aboutactive="",
                           projectsactive="",
                           contactsactive="",
                           skillsactive="active",
                            title="Skills",
                            os=os_info,
                            datetime=current_time,
                            user_agent=us_ag)
if __name__ == '__main__':
    app.run(debug=True)
