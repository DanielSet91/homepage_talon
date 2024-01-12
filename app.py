from flask import Flask
from modules.user import login_manager, db
from modules.routes import configure_routes
import secrets
from flask_mail import Mail

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\USER\\VsCode\\homepage_talon\\instance\\users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = secrets.token_hex(16)
app.config["SECRET_KEY"] = secret_key
app.config["SESSION_TYPE"] = "filesystem"

app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'Elessar.nazgul@gmail.com'
app.config['MAIL_PASSWORD'] = ''

mail = Mail(app)

db.init_app(app)

login_manager.init_app(app)

configure_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run(host="127.0.0.1", port=5000, debug=True)
