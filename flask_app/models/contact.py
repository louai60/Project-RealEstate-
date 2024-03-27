from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class Contact:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.message = data['message']
        self.created_at = data['created_at']
        self.sender_id = data["sender_id"]


    @classmethod
    def create(cls, data):
        query = "INSERT INTO contact (name, email, message, sender_id) VALUES (%(name)s, %(email)s, %(message)s, %(sender_id)s);"
        new_contact_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_contact_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM contact"
        results = connectToMySQL(DATABASE).query_db(query)
        contact_instances = []
        if results:
            for row in results:
                one_property = cls(row)  
                contact_instances.append(one_property)
            return contact_instances
        return []

    @classmethod
    def get_by_id(cls, contact_id):
        query = "SELECT * FROM contact WHERE id = %(id)s;"
        data = {'id': contact_id}
        return connectToMySQL(DATABASE).query_db(query, data)

    def update(self, data):
        query = "UPDATE contact SET name = %(name)s, email = %(email)s, message = %(message)s WHERE id = %(id)s;"
        self.db.query_db(query, data)

    @classmethod
    def delete(cls, contact_id):
        query = "DELETE FROM contact WHERE id = %(id)s;"
        data = {'id': contact_id}
        connectToMySQL(DATABASE).query_db(query, data)
