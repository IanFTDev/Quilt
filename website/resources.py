from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify, send_from_directory
from .models import Pattern, Project, Tile
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = os.path.abspath('server/patterns/')

DEFAULT_COLUMNS = 6
DEFAULT_ROWS = 6

resources = Blueprint('resources', __name__)

@resources.route('/dimensions-update/<int:project_id>', methods=['POST'])
@login_required
def update_dimensions(project_id):
    quiltHeight = request.form.get('quiltHeight')
    quiltWidth = request.form.get('quiltWidth')

    project = Project.query.get_or_404(project_id)

    # Validate input
    if not (quiltWidth.isdigit() and quiltHeight.isdigit()):
        flash("Input a positive number", category='error')
        return redirect(url_for('views.view_project', project_id=project_id))
    
    new_width = int(quiltWidth)
    new_height = int(quiltHeight)
    
    if new_width <= 0 or new_height <= 0:
        flash("Input a positive number", category='error')
        return redirect(url_for('views.view_project', project_id=project_id))

    # Delete tiles that are out of bounds
    tiles_to_delete = [tile for tile in project.tiles 
                       if tile.column >= new_width or tile.row >= new_height]
    
    for tile in tiles_to_delete:
        db.session.delete(tile)
    
    # Update dimensions
    project.columns = new_width
    project.rows = new_height
    
    # Create new tiles for expanded dimensions
    existing_positions = {(tile.column, tile.row) for tile in project.tiles}
    
    for x in range(new_width):
        for y in range(new_height):
            if (x, y) not in existing_positions:
                new_tile = Tile()
                new_tile.row = y
                new_tile.column = x
                project.tiles.append(new_tile)
    
    db.session.commit()
    
    return redirect(url_for('views.view_project', project_id=project_id))

@resources.route('/download-pattern', methods = ['POST'])
@login_required
def download_pattern():
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


    #populates the list of tiles
    for x in range(new_project.columns):
        for y in range(new_project.rows):
            new_tile = Tile()
            new_project.tiles.append(new_tile)
            new_tile.row = x
            new_tile.column = y

    db.session.commit()
    
    return jsonify({'success': True, 'project_id': new_project.id}), 200



@resources.route('/uploads/<path:filename>')
@login_required
def serve_upload(filename):

    return send_from_directory(UPLOAD_FOLDER, filename)

@resources.route('/uploads-tile-pattern/<int:pattern_id>')
@login_required
def serve_tile_pattern_request(pattern_id):
    pattern = Pattern.query.get_or_404(pattern_id)

    return serve_upload(pattern.image_path)


@resources.route('/save-tile', methods= ['POST'])
@login_required
def save_tile():
    print(request.form)
    tile_id = request.form['tile_id']
    pattern_id = request.form['pattern_id']

    tile = Tile.query.get_or_404(tile_id)

    tile.pattern_id = pattern_id
    db.session.commit()
    return jsonify({'success': True}), 200


