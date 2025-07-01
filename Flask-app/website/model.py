from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)#primary key column
    name = db.Column(db.String(80))
    email = db.Column(db.String(80),unique = True)
    password = db.Column(db.String(80)) 
    notes = db.relationship('Note')


class Note(db.Model):
    id = db.Column(db.Integer,primary_key = True)#primary key column
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True),default = func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


