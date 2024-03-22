from flask import Flask, abort, redirect, render_template, request, flash, session
from flask_app import app
from flask_app.models.property import Property
from flask_app.models.user import User



@app.route('/admin')
def dashboard():

    return render_template('admin/base.html')


@app.route('/admin/users')
def users():

    all_users = User.get_all()
    return render_template('admin/users.html', all_users = all_users)


@app.route('/admin/all_properties')
def all_properties():

    properties = Property.get_all()
    return render_template('admin/all_properties.html', properties = properties)



#! ACTION ROUTE (Delete recipe)
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):

    User.delete_user(id)
    return redirect('/admin/users')

#! ACTION ROUTE (Delete recipe)
@app.route('/delete_property/<int:id>', methods=['POST'])
def delete_property(id):
    
    Property.delete_property(id)
    return redirect('/admin/all_properties')
