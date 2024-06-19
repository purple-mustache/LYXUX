"""Python script to handle the table creation in db"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model):
    # the id column of the db table
    id = db.Column(db.Integer, primary_key=True)

    # the username column of the db table
    username = db.Column(db.String(150), unique=True, nullable=False)

    # the password column of the db table
    password = db.Column(db.String(150), nullable=False)


class TodoTable(db.Model):
    # the id column of the db table
    id = db.Column(db.Integer, primary_key=True)

    # the task column of the db table
    task = db.Column(db.String(200), nullable=False)

    # the checkbox column of the db table: for if task is completed
    complete = db.Column(db.Boolean, default=False)

    # user id of owner of the todo table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # user object
    user = db.relationship('User', backref=db.backref('todos', lazy=True))



