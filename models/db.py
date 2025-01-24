import mysql.connector
from config import DB_CONFIG

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            port=DB_CONFIG['port']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
