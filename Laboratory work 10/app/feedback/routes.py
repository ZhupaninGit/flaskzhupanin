from app.feedback import bp
from .form import FeedbackForm
from .model import Feedback
from flask import render_template,redirect,flash,url_for
from app import db

@bp.route('/feedback/',methods=["GET","POST"])
def feedback():
    feedback = FeedbackForm()
    feedback_list = Feedback.query.all()
    return render_template("feedback.html",active="Відгуки",title="Відгуки",form=feedback,feedback_list=feedback_list)

@bp.route("/add_feedback/",methods=["GET","POST"])
def add_feedback():
    feedback = FeedbackForm()
    feedback_list = Feedback.query.all()
    if feedback.validate_on_submit():
        newfeedback = Feedback(name=feedback.name.data, email=feedback.email.data, message=feedback.message.data)
        db.session.add(newfeedback)
        db.session.commit()
        flash("Відгук було успішно додано.","successs")    
        return redirect(url_for("feedback.feedback"))
    flash("Відгук не було додано.","error")    
    return render_template('feedback.html',
                                active="Відгуки",
                                form = feedback,
                                title="Відгуки",
                                feedback_list=feedback_list)