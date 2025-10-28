from flask import Blueprint, render_template, session, abort
from flask_login import login_required, current_user
from . import db
from .models import Project

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def projects():
    user_projects = current_user.projects

    return render_template('projects.html', user=current_user, user_projects = user_projects)



@views.route('/project/<int:project_id>', methods=['GET'])
@login_required
def view_project(project_id):    
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        abort(403)
    
    cols = project.columns
    rows = project.rows

    all_patterns = project.patterns

    all_tiles = project.tiles
    

    return render_template(
        "quilt_design.html",
        user=current_user,
        cols = cols,
        rows = rows ,
        projectID = project_id,
        all_patterns = all_patterns,
        all_tiles = all_tiles)

