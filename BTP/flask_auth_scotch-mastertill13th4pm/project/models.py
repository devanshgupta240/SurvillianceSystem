# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    # def __rep__(self):
    #     return f"User('{self.id}','{self.email}')"
class Post(db.Model):
    ip = db.Column(db.String(15), primary_key=True) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100))

    # def __rep__(self):
    #     return f"Post('{self.ip}','{self.password}')"

