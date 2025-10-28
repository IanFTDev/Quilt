from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    projects = db.relationship('Project', backref='user')



class Pattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    image_path = db.Column(db.String(255))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patterns = db.relationship('Pattern', backref='project')
    tiles = db.relationship('Tile', backref='project')
    columns = db.Column(db.Integer)
    rows = db.Column(db.Integer)


class Tile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pattern_id = db.Column(db.Integer, db.ForeignKey('pattern.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    column = db.Column(db.Integer)
    row = db.Column(db.Integer)


    
