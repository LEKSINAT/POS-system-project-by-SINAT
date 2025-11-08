# models/user_model.py
from . import get_db

class User:
    @staticmethod
    def create(name, email, password):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        db.commit()
        cur.close()

    @staticmethod
    def find_by_email_and_name(email, name):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = %s AND name = %s",
            (email, name)
        )
        user = cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def find_by_email_and_name_and_password(email, name, password):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = %s AND name = %s AND password = %s",
            (email, name, password)
        )
        user = cur.fetchone()
        cur.close()
        return user