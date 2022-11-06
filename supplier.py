from sqlite3 import connect
from dotenv import dotenv_values
from sqlite_commands import create_client_information_table
from sqlite_commands import create_group_information_table
from sqlite_commands import create_user_information_table


"""
Get all values from .env file and store in config variable
"""
config = dotenv_values(dotenv_path="./.env")


"""
Connect with SQLITE database file
"""
add_connection = connect(config.get("DATA_DB_PATH"))
add_cursor = add_connection.cursor()


"""
Creating basic tables in the database file
"""
add_cursor.execute(create_client_information_table)
add_cursor.execute(create_group_information_table)
add_cursor.execute(create_user_information_table)
