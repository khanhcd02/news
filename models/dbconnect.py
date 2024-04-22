import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "1234$",
            "database": "newsdb"
        }
        self.conn = mysql.connector.connect(**self.db_config)

    def get_connection(self):
        return self.conn

    def close_connection(self):
        self.conn.close()
        
    def cursor(self):
        return self.conn.cursor()
    
    def CRUD(self, query, params=None):
        cursor = self.conn.cursor()
        if(params):
            cursor.execute(query,params)
            if query.strip().upper().startswith("SELECT"):
                data = cursor.fetchall()
                data = [dict(zip(cursor.column_names, row)) for row in data]
                cursor.close()
                return data
            self.conn.commit()
            cursor.close()
        else:
            cursor.execute(query)
            data = cursor.fetchall()
            data = [dict(zip(cursor.column_names, row)) for row in data]
            cursor.close()
            return data
        