from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify
from .models import Pattern, Project, Tile
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import boto3
from botocore.exceptions import ClientError

S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
S3_REGION = os.environ.get('AWS_REGION', 'us-east-1')


def _s3():
    return boto3.client('s3', region_name=S3_REGION)


def _presigned_url(s3_key, expiry=3600):
    try:
        return _s3().generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': s3_key},
            ExpiresIn=expiry
        )
    except ClientError:
        return None

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

    new_pattern = Pattern()
    db.session.add(new_pattern)
    db.session.flush()

    name, ext = os.path.splitext(filename)
    s3_key = f"user_{current_user.id}/project_{projectID}/{name}_{new_pattern.id}{ext}"
    new_pattern.image_path = s3_key

    project = Project.query.get(projectID)
    project.patterns.append(new_pattern)
    db.session.commit()

    _s3().upload_fileobj(file, S3_BUCKET, s3_key)

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
    url = _presigned_url(filename)
    if url is None:
        return jsonify({'error': 'File not found'}), 404
    return redirect(url)

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


