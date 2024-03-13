from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

# Regular expression for the email format
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

class User:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        try:
            return connectToMySQL(DATABASE).query_db(query, data)
        except Exception as e:
            flash(f"Error creating user: {str(e)}", "register_error")
            return False

    @classmethod
    def get_by_email(cls, data):
        query = """
                    SELECT * FROM users
                    WHERE email = %(email)s;
            """
        try:
            result = connectToMySQL(DATABASE).query_db(query, data)
            if result:
                return User(result[0])
            else:
                return None
        except Exception as e:
            flash(f"Error fetching user by email: {str(e)}", "user_error")
            return None

    @classmethod
    def get_by_id(cls, data):
        query = """
                    SELECT * FROM users
                    WHERE id = %(id)s;
            """
        try:
            result = connectToMySQL(DATABASE).query_db(query, data)
            if result:
                return User(result[0])
            else:
                return None
        except Exception as e:
            flash(f"Error fetching user by ID: {str(e)}", "user_error")
            return None

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data["first_name"]) < 1:
            is_valid = False
            flash("First name is required!", "register")

        if len(data["last_name"]) < 1:
            is_valid = False
            flash("Last name is required!", "register")

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
            flash("Email is required!", "login")
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "login")
            is_valid = False

        if len(data["password"]) < 1:
            is_valid = False
            flash("Password is required!", "login")

        return is_valid

    