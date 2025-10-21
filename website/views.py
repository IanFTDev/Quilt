from flask import Blueprint, render_template, session
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():

    if 'quilt_height' not in session:
        session['quilt_height'] = 2
    if 'quilt_width' not in session:
        session['quilt_width'] = 2
    return render_template("quilt_design.html", user=current_user, cols = session['quilt_width'], rows = session['quilt_height'])