from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

# Regular expression for the email format
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data):
        self.id = data["user_id"]
        self.username = data["username"]
        self.email = data["email"]
        self.phone = data["phone"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.is_admin = data["is_admin"] 
        self.address = data["address"]

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO users (username, email, phone, password, is_admin)
                VALUES(%(username)s, %(email)s, %(phone)s, %(password)s, %(is_admin)s);
                """
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id
      

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
       
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return User(result[0])
        else:
            return None

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE user_id = %s;"
        result = connectToMySQL(DATABASE).query_db(query, (user_id,))

        if result:
            return cls(result[0])
        else:
            return None

      
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(DATABASE).query_db(query)
        users_instances = []
        if results:
            for row in results:
                one_user = cls(row)  
                users_instances.append(one_user)
            return users_instances
        return []
        

        
    #* =========== UPDATE ===========

    @classmethod
    def update(cls, data):
        query = """
                UPDATE users
                SET username = %(username)s, email = %(email)s, phone = %(phone)s, address = %(address)s
                WHERE user_id = %(id)s;
                """

        return connectToMySQL(DATABASE).query_db(query, data)
    
     #* =========== DELETE ===========
    @classmethod
    def delete_user(cls, id):
        query = "DELETE FROM users WHERE user_id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query, {'id': id})



    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data["username"]) < 1:
            is_valid = False
            flash("username is required!", "register")

        if len(data["email"]) < 1:
            is_valid = False
            flash("Email is required!", "register")
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "register")
            is_valid = False
        else:
            email_dict = {"email": data["email"]}
            potential_user = User.get_by_email(email_dict)
            if potential_user:
                is_valid = False
                flash("This email is already taken!", "register")

        if len(data["phone"]) < 8:
            is_valid = False
            flash("Phone is required!", "register")

        if len(data["password"]) < 1:
            is_valid = False
            flash("Password is required!", "register")
        elif data["password"] != data["confirm_password"]:
            is_valid = False
            flash("Passwords don't match!", "register")

        return is_valid

    @staticmethod
    def validate_login_user(data):
        is_valid = True

        if len(data["email"]) < 1:
            is_valid = False
            flash("Email is required!", "danger")
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "danger")
            is_valid = False

        if len(data["password"]) < 8:
            is_valid = False
            flash("Password is required!", "danger")

        return is_valid

    
    @classmethod
    def get_user_by_id(cls, mysql, user_id):
        query = "SELECT * FROM users WHERE user_id = %s;"
        result = mysql.query_db(query, (user_id,))
        if result:
            return cls(result[0])
        else:
            return None
        
    