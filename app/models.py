from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(40))
    password = db.Column(db.String(255))
    comments = db.relationship('Comment') #facilita la relacion entre dos tablas
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.__create_password(password)


    def __create_password(self, password):
        return generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model):
    __tablename__ = 'Comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #manejo de relaciones entre tablas 
    text = db.Column(db.Text())
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
