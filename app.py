from flask import Flask, render_template, redirect, request, session, flash
from flask_login import current_user, LoginManager, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = secrets.token_hex(16)
app.config["SECRET_KEY"] = secret_key
app.config["SESSION_TYPE"] = "filesystem"

login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.session_protection = "strong" 

db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def get_id(self):
        return str(self.id)
    


@app.route("/")
def index():
    print("current user: ", current_user)
    return render_template("index.html", current_user=current_user)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("register-username")
        username = username.lower()
        password = request.form.get("register-password")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already in use.", "error")
            return redirect("/register")
            
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect("/")
        else:
            flash("Wrong username or password", "error")
    return render_template("login.html")

@app.route("/profile")
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user= user)

@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    print("User logged out")

    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="127.0.0.1", port=5000, debug=True)
