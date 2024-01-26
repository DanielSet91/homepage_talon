from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from modules.utilys import mail
import os
import secrets
from modules.user import User, db
from modules.routes import configure_routes

mysql = MySQL()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder='templates')

    # MySQL configurations
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USERNAME')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')
    mysql.init_app(app)

    # SQLALCHEMY configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost/talon_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Other configurations
    secret_key = secrets.token_hex(16)
    app.config["SECRET_KEY"] = secret_key
    app.config["SESSION_TYPE"] = "filesystem"

    # Mail configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'
    mail.init_app(app)

    # Login manager configuration
    login_manager.init_app(app)
    login_manager.login_view = 'login' 
    login_manager.session_protection = "strong" 
    
    db.init_app(app)

    # CSRF protection
    csrf.init_app(app)

    # Migrate configuration
    migrate = Migrate(app, db)

    configure_routes(app)

    # Register the load_user function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app, db

if __name__ == "__main__":
    app, db = create_app()
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run(host="127.0.0.1", port=5000, debug=True)
