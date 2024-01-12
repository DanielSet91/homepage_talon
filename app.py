from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from modules.user import login_manager
from modules.routes import configure_routes
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\USER\\VsCode\\homepage_talon\\instance\\users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = secrets.token_hex(16)
app.config["SECRET_KEY"] = secret_key
app.config["SESSION_TYPE"] = "filesystem"


db = SQLAlchemy(app)
login_manager.init_app(app)

configure_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run(host="127.0.0.1", port=5000, debug=True)
