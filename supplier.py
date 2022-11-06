from sqlite3 import connect
from dotenv import dotenv_values


"""
Get all values from .env file and store in config variable
"""
config = dotenv_values(dotenv_path="./.env")


"""
Connect with SQLITE database file
"""
add_connection = connect(config.get("DATA_DB_PATH"))
add_cursor = add_connection.cursor()

