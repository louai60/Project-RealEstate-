from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def process_register():
    if not User.validate_user(request.form):
        flash("Invalid registration data", "register_error")
        return redirect("/")
    
    try:
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {**request.form, "password": pw_hash}
        user_id = User.create(data)
        session["user_id"] = user_id
        return redirect("/recipes")
    except Exception as e:
        flash(f"Error during registration: {str(e)}", "register_error")
        return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    if not User.validate_login_user(request.form):
        flash("Invalid login data", "login_error")
        return redirect("/")

    user_in_db = User.get_by_email({"email": request.form["email"]})
    
    if not user_in_db:
        flash("Invalid Email/Password", "login_error")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password", "login_error")
        return redirect("/")

    session["user_id"] = user_in_db.id
    return redirect("/recipes")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
