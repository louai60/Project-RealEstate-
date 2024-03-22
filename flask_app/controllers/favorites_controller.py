from flask_app import DATABASE, app
from flask import Blueprint, render_template, request, jsonify
from flask_app.models.user import User
from flask_app.models.property import Property
from flask_app.models.favorites import Favorites
from flask_login import current_user, login_required  



@app.route('/favorites', methods=['GET'])
def display_favorites():
    # You can add logic here to fetch the user's favorite properties from the database
    # For demonstration purposes, let's assume you have a list of favorite properties
    favorite_properties = Favorites.get_all()

    # Render the favorites HTML template and pass the favorite properties to it
    return render_template('favorites.html', favorite_properties=favorite_properties)


@app.route('/favorites/add', methods=['POST'])
def add_to_favorites():
    property_id = request.json.get('property_id')
    user_id = current_user.id
    
    if not property_id:
        return jsonify({'error': 'Property ID is required.'}), 400
    
    property = Property.query.get(property_id)
    user = User.query.get(user_id)
    
    if not property or not user:
        return jsonify({'error': 'Property or user not found.'}), 404
    
    if Favorites.query.filter_by(user_id=user_id, property_id=property_id).first():
        return jsonify({'error': 'Property already in favorites.'}), 400
    
    favorite = Favorites(user_id=user_id, property_id=property_id)
    DATABASE.session.add(favorite)
    DATABASE.session.commit()
    
    return jsonify({'message': 'Property added to favorites successfully.'}), 200

@app.route('/favorites/remove', methods=['POST'])
def remove_from_favorites():
    property_id = request.json.get('property_id')
    user_id = current_user.id
    
    if not property_id:
        return jsonify({'error': 'Property ID is required.'}), 400
    
    favorite = Favorites.query.filter_by(user_id=user_id, property_id=property_id).first()
    
    if not favorite:
        return jsonify({'error': 'Property not found in favorites.'}), 404
    
    DATABASE.session.delete(favorite)
    DATABASE.session.commit()
    
    return jsonify({'message': 'Property removed from favorites successfully.'}), 200
