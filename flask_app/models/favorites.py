from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models.user import User
from flask_app.models.property import Property

class Favorites:
    def __init__(self, data):
        self.id = data["favorites_id"]
        self.user_id = data["user_id"]
        self.property_id = data["property_id"]
        self.created_at = data["created_at"]

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO favorites (user_id, property_id, created_at)
                VALUES (%(user_id)s, %(property_id)s, %(created_at)s)
                """
        favorites_id = connectToMySQL(DATABASE).query_db(query, data)
        return favorites_id
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM favorites"
        results = connectToMySQL(DATABASE).query_db(query)
        favorites_instances = []
        if results:
            for row in results:
                one_property = cls(row)  
                favorites_instances.append(one_property)
            return favorites_instances
        return []