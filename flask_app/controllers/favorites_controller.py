from flask_app import app, DATABASE
from flask import render_template, redirect, flash, session, url_for
from flask_app.models.user import User
from flask_app.models.property import Property
from flask_app.models.favorites import Favorites

@app.route('/favorites', methods=['GET'])
def display_favorites():
    if 'user_id' not in session:
        flash('Please log in to view favorite properties.', 'error')
        return redirect(url_for('login'))
    
 
    user_id = session['user_id']
    favorite_properties = Favorites.get_favorite_properties(user_id) 
    num_favorites = len(favorite_properties)  
    session['num_favorites'] = num_favorites


    # one_property = Property.get_one_with_user(data)

    return render_template('favorites.html', favorite_properties=favorite_properties, property=Property, num_favorites=num_favorites)



@app.route('/add_favorite/<int:property_id>', methods=['POST'])
def add_favorite(property_id):
    if 'user_id' not in session:
        flash('Please log in to add properties to favorites.', 'error')
        return redirect(url_for('login'))
    
    data = {
        "user_id": session['user_id'],
        "property_id": property_id
    }

    result = Favorites.add_to_favorites(data)
    if result:
        flash('Property added to favorites.', 'success')
    else:
        flash('Failed to add property to favorites.', 'error')

    return redirect(url_for('properties', property_id=property_id))

@app.route('/delete_favorite/<int:id>', methods=['POST'])
def delete_favorite(id):
    # if "is_admin" not in session:
    #     flash("Only Admin Can Access Dashboard.", "danger")
    #     return redirect("/")
    
    Favorites.delete_favorite(id)
    return redirect('/favorites')