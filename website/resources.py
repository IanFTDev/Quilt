from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify, send_from_directory
from .models import Pattern, Project
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'server/patterns/'

DEFAULT_COLUMNS = 6
DEFAULT_ROWS = 6

resources = Blueprint('resources', __name__)


@resources.route('/dimensions-update/<int:project_id>', methods = ['POST'])
@login_required
def update_dimensions(project_id):
    quiltHeight = request.form.get('quiltHeight')
    quiltWidth = request.form.get('quiltWidth')


    project = Project.query.get_or_404(project_id)

    if quiltWidth.isdigit() and quiltHeight.isdigit():
        if int(quiltHeight) > 0 and int(quiltWidth) > 0:
            project.columns = int(quiltWidth)
            project.rows = int(quiltHeight)
            db.session.commit()
            return redirect(url_for('views.view_project', project_id=project_id))
        else:
            flash("Input a positive number", category='error')
    else:
        flash("Input a postive number", category='error')
    

    return redirect(url_for('views.view_project', project_id=project_id))


@resources.route('/upload-pattern', methods = ['POST'])
@login_required
def upload_pattern():
    file = request.files['image']
    projectID = request.form['projectID']
    filename = secure_filename(file.filename)
  
    
    user_upload_folder = os.path.join(f"user_{current_user.id}", f"project_{projectID}")
    os.makedirs(os.path.join(UPLOAD_FOLDER, user_upload_folder), exist_ok=True)


    # Store the path relative to your server
    new_pattern = Pattern()
    db.session.add(new_pattern)
    db.session.flush()
    filepath = user_upload_folder + '/' + filename
    name, ext = os.path.splitext(filepath)
    filepath = f"{name}_{new_pattern.id}{ext}"

    new_pattern.image_path = filepath
    

    project = Project.query.get(projectID)
    # Add pattern to project using the relationship
    project.patterns.append(new_pattern)

    db.session.commit()
    
    # Save to YOUR server's filesystem
    file.save(os.path.join(UPLOAD_FOLDER, filepath))



    return jsonify({'success': True, 'pattern_id': new_pattern.id}), 200



@resources.route('/create-project', methods=['POST'])
@login_required
def create_project():
    # Create new project in database
    new_project = Project(user_id=current_user.id, columns=DEFAULT_COLUMNS, rows=DEFAULT_ROWS)
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({'success': True, 'project_id': new_project.id}), 200



@resources.route('/uploads/<path:filename>')
@login_required
def serve_upload(filename):
    print(UPLOAD_FOLDER + filename)
    return send_from_directory(UPLOAD_FOLDER, filename)
