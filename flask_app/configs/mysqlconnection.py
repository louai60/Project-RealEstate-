# flask_app/configs/mysqlconnection.py
import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        self.connection = connection

    def query_db(self, query, data=None, one=False):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, data)
                if query.lower().startswith('select'):
                    if one:
                        result = cursor.fetchone()
                    else:
                        result = cursor.fetchall()
                    return result
                elif query.lower().startswith('insert'):
                    self.connection.commit()
                    return cursor.lastrowid
                else:
                    self.connection.commit()
            except Exception as e:
                print("Error executing query:", e)
                self.connection.rollback()
                return False

# connectToMySQL function remains unchanged
def connectToMySQL(db):
    return MySQLConnection(db)
