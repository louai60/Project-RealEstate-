from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, json
from flask_app.models.user import User

class Property:
    def __init__(self, data):
        self.id = data["property_id"]
        self.title = data["title"]
        self.type = data["type"]
        self.description = data["description"]
        self.address = data["address"]
        self.bedrooms = data["bedrooms"]
        self.bathrooms = data["bathrooms"]
        self.space = data["space"]
        self.status = data["status"]
        self.price = data["price"]
        self.image_paths = data["image_paths"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.seller_id = data["seller_id"]

    # @classmethod
    # def create(cls, data):
    #     query = """
    #             INSERT INTO properties (title, description, type, price, address, bedrooms, bathrooms, space,  status, image_paths, seller_id)
    #             VALUES (%(title)s, %(description)s, %(type)s, %(price)s, %(address)s, %(bedrooms)s, %(bathrooms)s, %(space)s, %(status)s, %(image_paths)s, %(seller_id)s)
    #             """
    #     property_id = connectToMySQL(DATABASE).query_db(query, data)
    #     return property_id
    
    # @classmethod
    # def create(cls, data):
    #     image_paths = ', '.join(['%s'] * len(data['image_paths']))
    #     query = """
    #             INSERT INTO properties (title, description, type, price, address, bedrooms, bathrooms, space, status, image_paths, seller_id)
    #             VALUES (%(title)s, %(description)s, %(type)s, %(price)s, %(address)s, %(bedrooms)s, %(bathrooms)s, %(space)s, %(status)s, """ + image_paths + """, %(seller_id)s)
    #             """
    #     property_id = connectToMySQL(DATABASE).query_db(query, data)
    #     return property_id
        
    @classmethod
    def create(cls, data):
        image_paths_json = json.dumps(data['image_paths'])
        
        query = """
                INSERT INTO properties (title, description, type, price, address, bedrooms, bathrooms, space, status, image_paths, seller_id)
                VALUES (%(title)s, %(description)s, %(type)s, %(price)s, %(address)s, %(bedrooms)s, %(bathrooms)s, %(space)s, %(status)s, %(image_paths)s, %(seller_id)s)
                """
        
        data['image_paths'] = image_paths_json
        
        property_id = connectToMySQL(DATABASE).query_db(query, data)
    
        return property_id
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM properties"
        results = connectToMySQL(DATABASE).query_db(query)
        properties_instances = []
        if results:
            for row in results:
                one_property = cls(row)  
                properties_instances.append(one_property)
            return properties_instances
        return []
    
    #* =========== GET BY ID ===========
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM properties WHERE property_id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])  
        else:
            return None
    
    @classmethod
    def get_one_with_user(cls, data):
        query = """
            SELECT * FROM properties
            JOIN users ON properties.seller_id = users.user_id
            WHERE properties.property_id = %(id)s
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result or len(result) == 0:
            return None 

        row = result[0]

        current_property = Property(row)

        user_fixed = {
            **row,
            "id": row["user_id"],  
            "created_at": row["created_at"],  
            "updated_at": row["updated_at"]  
        }

        current_property.posted_by = User(user_fixed)

        return current_property
    
    
    # @classmethod
    # def search_records(cls, query):
    #     query = f"SELECT * FROM properties WHERE title LIKE '%{query}%' OR status LIKE '%{query}%'"
    #     results = connectToMySQL(DATABASE).query_db(query)
    #     return results

    @classmethod
    def search_records(cls, location=None, property_type=None, property_status=None, price_limit=None):
        query = "SELECT * FROM properties WHERE 1=1"
        params = {}

        if location:
            query += " AND address LIKE %(location)s"
            params['location'] = f"%{location}%"

        if property_type:
            query += " AND property_type = %(property_type)s"
            params['property_type'] = property_type

        if property_status:
            query += " AND status = %(property_status)s"
            params['property_status'] = property_status

        if price_limit:
            query += " AND price <= %(price_limit)s"
            params['price_limit'] = price_limit

        results = connectToMySQL(DATABASE).query_db(query, params)
        return results
    

    #* =========== DELETE ===========
    @classmethod
    def delete_property(cls, id):
        query = "DELETE FROM properties WHERE property_id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query, {'id': id})


    @staticmethod
    def validate_property(data):
        is_valid = True

        if len(data["title"]) < 1:
            is_valid = False
            flash("title is required!", "danger")

        if len(data["description"]) < 1:
            is_valid = False
            flash("description is required!", "danger")
        
        if len(data["price"]) < 1:
            is_valid = False
            flash("price is required!", "danger")
        
        if len(data["address"]) < 1:
            is_valid = False
            flash("address is required!", "danger")
        
        if len(data["bedrooms"]) < 1:
            is_valid = False
            flash("Number of Bedrooms is required!", "danger")

        if len(data["bathrooms"]) < 1:
            is_valid = False
            flash("Number of bathrooms is required!", "danger")


        return is_valid