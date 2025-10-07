from flask import Blueprint, render_template, session
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    if session['quilt_height'] == None:
        session['quilt_height'] = 2
    if session['quilt_width'] == None:
        session['quilt_width'] = 2
    return render_template("quilt_design.html", user=current_user, cols = session['quilt_width'], rows = session['quilt_height'])