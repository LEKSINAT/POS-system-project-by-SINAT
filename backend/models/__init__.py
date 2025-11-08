# models/__init__.py
from flask import current_app

def get_db():
    """Return the MySQL connection from the Flask app."""
    return current_app.mysql.connection