from flask import Flask, abort, redirect, render_template, request, flash, session
from flask_app import app
from flask_app.models.property import Property
from flask_app.models.user import User
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '../static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route("/")
# def layout():
#     # Guard Route
#     if "user_id" not in session:
#         flash("You are not logged in.", "danger")
#         return redirect("/login")

#     user_id = session["user_id"]
#     user_data = User.get_by_id(user_id)

#     if not user_data:
#         flash("User data not found.", "danger")
#         return redirect("/")

#     return render_template("layout.html", user=user_data)



@app.route('/')
def view_home():

    # user_id = session["user_id"]
    # user_data = User.get_by_id(user_id)
    return render_template('home.html')

@app.route('/', methods=['POST'])
def handle_search():
    location = request.form.get('location')
    property_type = request.form.get('property_type')
    property_status = request.form.get('property_status')
    price_limit = request.form.get('price_limit')

    results = Property.search_records(location, property_type, property_status, price_limit)
    if results:
        return render_template('home.html', results=results)
    else:
        flash('Property not found.', 'danger')
        return redirect('/')




@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/property/<int:id>')
def view_property(id):
    
    if "user_id" not in session:
        flash("You need to be logged to see a property.", "danger")
        return redirect("/properties")

    data = {
        "id": id
    }

    one_property = Property.get_one_with_user(data)
    return render_template('property.html', property=Property.get_by_id(data), creator=one_property)

# @app.route('/properties')
# def display_properties():
#     all_properties = Property.get_all()
#     return render_template('properties.html', all_properties=all_properties)


@app.route('/properties')
def properties():

    status = request.args.get('status')
    all_properties = []

    if status == 'for_sell':
        all_properties = Property.search_records(property_status='For Sell')
    elif status == 'for_rent':
        all_properties = Property.search_records(property_status='For Rent')
    else:
        all_properties = Property.get_all()
        
    return render_template('properties.html', all_properties=all_properties)



@app.route("/add_property", methods=['GET', 'POST'])
def display_create_property():
    if "user_id" not in session:
        flash("You need to be logged in to add a property.", "danger")
        return redirect("/")

    if request.method == 'POST':
        # Check if a property is valid
        if not Property.validate_property(request.form):
            flash("Invalid property data!", "danger")
            return redirect('/add_property')  
        
        selected_status = request.form.get('status')

        data = {
            **request.form,
            "seller_id": session["user_id"],
            "status": selected_status
        }
        id = Property.create(data)  
        flash("Property added successfully!", "success")
        return redirect(f'/property/{id}')

    return render_template("add_property.html")


