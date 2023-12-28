from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def get_id(self):
        return str(self.id)

login_manager = LoginManager()
login_manager.login_view = 'login' 
login_manager.session_protection = "strong" 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
