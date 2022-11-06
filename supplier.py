from dotenv import dotenv_values


"""
Get all values from .env file and store in config variable
"""
config = dotenv_values(dotenv_path="./.env")

