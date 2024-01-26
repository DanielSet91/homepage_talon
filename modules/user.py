from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    user_info = db.relationship('UserInfo', back_populates='user', uselist=False)
    
    def get_id(self):
        return str(self.id)


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    favorite_genres = db.Column(db.String(255), nullable=True)
    favorite_instrument = db.Column(db.String(255), nullable=True)
    job = db.Column(db.String(255), nullable=True)
    
    twitter = db.Column(db.String(255), nullable=True)
    facebook = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='user_info')

    @classmethod
    def create_tables(cls):
        with db.app.app_context():
            db.create_all()
