from pprint import pprint
from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route("/register")
def show_register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def process_register():
    if request.method == "POST":
        if not User.validate_user(request.form):
            return redirect("/register")
        
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            **request.form,
            "password": pw_hash,
            "is_admin": False  
        }

        if request.form["email"] == "admin@gmail.com" and request.form["password"] == "password":
            data["is_admin"] = True

        user_id = User.create(data)
        session["user_id"] = user_id
        session["username"] = data["username"]
        session["email"] = data["email"]
        session["user_is_admin"] = data["is_admin"]

        new_user = User.get_by_id(user_id)
        notify_admin(f"{new_user.username} registered")
        
        flash(f"Success: welcome {new_user.username}", "success")
        
        if data["is_admin"]:
            return redirect("/admin/users")  
        else:
            return redirect("/")
    
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    if not User.validate_login_user(request.form):
        return redirect("/login")

    user_in_db = User.get_by_email({"email": request.form["email"]})
    
    if not user_in_db:
        flash("Invalid Email/Password", "danger")
        return redirect("/login")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password", "danger")
        return redirect("/login")

    session["user_id"] = user_in_db.id
    session["user_is_admin"] = user_in_db.is_admin
    session["username"] = user_in_db.username
    session["email"] = user_in_db.email

    notify_admin(f"{user_in_db.username} logged in")

  
    flash(f"Success: welcome {user_in_db.username} ", "success")
    
    if user_in_db.is_admin:
        return redirect("/admin/users")
    else:
        return redirect("/")



@app.route("/logout")
def logout():
    session.clear()
    notify_admin("User logged Out")
    return redirect("/")


@app.route("/account")
def user_account():
    # Guard Route
    if "user_id" not in session:
        flash("You are not logged in.", "danger")
        return redirect("/login")

    user_id = session["user_id"]
    user_data = User.get_by_id(user_id)

    if not user_data:
        flash("User data not found.", "danger")
        return redirect("/")

    return render_template("user_acc.html", user=user_data)

@app.route('/user/update/<int:id>', methods=['POST'])
def process_updated_user(id):
    #! Guard Route
    if "user_id" not in session:
        return redirect("/")
    
    # Grab the user id from the session
    data = {
        **request.form,
        "user_id": session["user_id"],
        "id": id
    }
    # Update the user to the database 
    User.update(data)

    return redirect('/account')



     
def notify_admin(message):
    session.setdefault("admin_notifications", []).append(message)
