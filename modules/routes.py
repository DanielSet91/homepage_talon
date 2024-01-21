from flask import render_template, redirect, request, session, flash, url_for, current_app
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from modules.user import User, db
from .forms import ContactForm
from flask_mail import Message
from modules.utilys import mail
from modules.userinfo import db as userInfo

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

            flash("Registration successful! Please log in.", "success")
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

    @app.route("/profile", methods=["Get"])
    @login_required
    def profile():
        user = current_user
        return render_template("profile.html", user= user)
    
    @app.route('/update_user_info', methods=["POST"])
    def update_user_info():
        user_full_name = request.form.get('user_full_name')
        user_email = request.form.get('user_email')

        user_info = userInfo.Query.first()

        user_info.name = user_full_name
        user_info.email = user_email

        db.session.commit()

        return(redirect(url_for('profile')))
    
    @app.route("/contact", methods =["GET", "POST"])
    def contact():
        print("Entering /contact route")
        if request.method == "POST":
            form = ContactForm()
            sender=request.form['Email']
            name = request.form['Name']
            subject = request.form['Subject']
            body = f'Sender: {sender}\nName: {name}\n\n{request.form["Message"]}'
            msg = Message(subject=subject, recipients=['elessar.nazgul@gmail.com'], body=body)
            try:
                mail.send(msg)
                return render_template('success.html')
            except Exception as e:
                return f'Error: {str(e)}'
        return render_template('index.html', form=form)

    @app.route("/success")
    def success():
        return render_template('success.html')
    
    @app.route("/music")
    def music():
        return render_template("music.html")
    
    @app.route("/logout")
    def logout():
        logout_user()
        session.clear()
        print("User logged out")

        return redirect("/")
