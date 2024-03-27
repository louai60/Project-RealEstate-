from flask import Flask, abort, json, redirect, render_template, request, flash, session
from flask_app import app
from flask_app.models.contact import Contact
from flask_app.models.property import Property
from flask_app.models.user import User



# @app.route('/admin')
# def dashboard():
#     # if "is_admin" not in session:
#     #     flash("Only Admin Can Access Dashboard.", "danger")
#     #     return redirect("/")

#     return render_template('admin/base.html')


@app.route('/admin/users')
def users():
    # if "is_admin" not in session:
    #     flash("Only Admin Can Access Dashboard.", "danger")
    #     return redirect("/")

    all_users = User.get_all()
    return render_template('admin/users.html', all_users = all_users)


@app.route('/admin/all_properties')
def all_properties():
    # if "is_admin" not in session:
    #     flash("Only Admin Can Access Dashboard.", "danger")
    #     return redirect("/")

    properties = Property.get_all()
    for property in properties:
        property.image_paths = json.loads(property.image_paths)
    return render_template('admin/all_properties.html', properties = properties)


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    # if "is_admin" not in session:
    #     flash("Only Admin Can Access Dashboard.", "danger")
    #     return redirect("/")

    User.delete_user(id)
    return redirect('/admin/users')

@app.route('/delete_property/<int:id>', methods=['POST'])
def delete_property(id):
    # if "is_admin" not in session:
    #     flash("Only Admin Can Access Dashboard.", "danger")
    #     return redirect("/")
    
    Property.delete_property(id)
    return redirect('/admin/all_properties')



@app.route('/admin/messages')
def messages():
    # if "is_admin" not in session:
    #     flash("Only Admin Can Access Dashboard.", "danger")
    #     return redirect("/")

    messages = Contact.get_all()
    return render_template('admin/messages.html', messages = messages)

