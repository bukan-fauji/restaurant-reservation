import mysql.connector
from config import DB_CONFIG

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)
