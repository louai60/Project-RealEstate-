from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Category:
    def __init__(self, data):
        self.id = data["property_id"]
        self.category = data["category"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
       