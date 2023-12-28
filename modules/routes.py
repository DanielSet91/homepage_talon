from flask import render_template, redirect, request, session, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from modules.user import User, db

def configure_routes(app):
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
