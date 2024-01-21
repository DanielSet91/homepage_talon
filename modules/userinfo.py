from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable= True)
    email = db.Column(db.String(255), unique = True, nullable=True)
    mobile = db.Column(db.String(255), unique=True, nullable=True)
    address = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique= True)
    user = db.relationship('User', back_populates='user_info')
    