from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from .models import Pattern
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'server/patterns/'

resources = Blueprint('resources', __name__)


@resources.route('/dimensions-update', methods = ['POST'])
@login_required
def update_dimensions():
    quiltHeight = request.form.get('quiltHeight')
    quiltWidth = request.form.get('quiltWidth')

    if quiltWidth.isdigit() and quiltHeight.isdigit():
        if int(quiltHeight) > 0 and int(quiltWidth) > 0:
            session['quilt_height'] = quiltHeight
            session['quilt_width'] = quiltWidth
            return redirect(url_for('views.home'))
        else:
            flash("Input a positive number", category='error')
    else:
        flash("Input a postive number", category='error')

    return redirect(url_for('views.home'))


# @resources.route('/upload-pattern', methods = ['POST'])
# def upload_pattern():
#     file = request.files['image']
#     filename = secure_filename(file.filename)

#     # Store the path relative to your server
#     new_pattern = Pattern(image_path=filepath)
#     db.session.add(new_pattern)
#     db.session.commit()


#     # Save to YOUR server's filesystem
#     filepath = os.path.join(UPLOAD_FOLDER, f"pattern_{new_pattern.id}_{filename}")
#     file.save(filepath)

#     return




# @resources.route('/pattern/<int:id>')
# def view_pattern(id):
#     pattern = Pattern.query.get_or_404(id)

#     return render_template('pattern.html', image_path=pattern.image_path)