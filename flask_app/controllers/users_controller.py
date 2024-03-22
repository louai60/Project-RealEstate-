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
            "password": pw_hash
        }

       
        session["user_id"] = User.create(data)
        # pprint("!!!!!!!!!!!!!!!!!!!!!!!!!!",user_id)

        # new_user = User.get_by_id(user_id)
        # print("////////////////////////////",user_id)
        # flash(f"Success: welcome {new_user.username}", "success")
        
      
        return redirect("/")
    
    return render_template("register.html")

# @app.route("/register", methods=["GET", "POST"])
# def process_register():
#     if request.method == "POST":
#         if not User.validate_user(request.form):
#             return redirect("/register")
        
#         pw_hash = bcrypt.generate_password_hash(request.form["password"])
#         data = {
#             **request.form,
#             "password": pw_hash
#         }

#         user_id = User.create(data)
#         print("--------------------------", user_id)  
        
#         session["user_id"] = user_id
#         print("**************************", session)  

#         flash("Success: User registered and logged in", "success")
#         return redirect("/")
      
#     return render_template("register.html")

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

  
    flash(f"Success: welcome {user_in_db.username} ", "success")
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
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
