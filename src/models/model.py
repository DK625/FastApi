from importlib_metadata import email
from sqlalchemy.orm import deferred

from ..config.connect_db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, description, email):
        self.name = name
        self.description = description
        self.email = email


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    due_date = db.Column(db.String(100))
    # status = db.Column(db.String(100), defauct="Unfinished")
    status = db.Column(db.String(100), default="Unfinished")
    email = db.Column(db.String(100))
    list_name = db.Column(db.String(100))
    # finished_at = db.Column(db.DateTime, default=datetime.now)
    finished_at = db.Column(db.DateTime)

    def __init__(self, title, description, due_date, status, email, list_name, finised_at):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.email = email
        self.list_name = list_name
        self.finished_at = finised_at
