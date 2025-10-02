from flask import Blueprint, render_template, request, flash
from .models import Pattern
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'server/patterns/'

resources = Blueprint('resources', __name__)



@resources.route('/upload-pattern', methods = ['POST'])
def upload_pattern():
    file = request.files['image']
    filename = secure_filename(file.filename)

    # Store the path relative to your server
    new_pattern = Pattern(image_path=filepath)
    db.session.add(new_pattern)
    db.session.commit()


    # Save to YOUR server's filesystem
    filepath = os.path.join(UPLOAD_FOLDER, f"pattern_{new_pattern.id}_{filename}")
    file.save(filepath)

    return




@resources.route('/pattern/<int:id>')
def view_pattern(id):
    pattern = Pattern.query.get_or_404(id)

    return render_template('pattern.html', image_path=pattern.image_path)