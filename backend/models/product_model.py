# models/product_model.py
from . import get_db

class Product:
    @staticmethod
    def all():
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        cur.close()
        return products

    @staticmethod
    def search_by_name(name_query):
        db = get_db()
        cur = db.cursor()
        like = f"%{name_query}%"
        cur.execute(
            "SELECT * FROM products WHERE product_name LIKE %s",
            (like,)
        )
        products = cur.fetchall()
        cur.close()
        return products

    @staticmethod
    def find(product_id):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cur.fetchone()
        cur.close()
        return product

    @staticmethod
    def create(name, price, stock):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO products (product_name, price, stock) VALUES (%s, %s, %s)",
            (name, price, stock)
        )
        db.commit()
        cur.close()

    @staticmethod
    def update(product_id, name, price, stock):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            UPDATE products
            SET product_name = %s, price = %s, stock = %s
            WHERE product_id = %s
            """,
            (name, price, stock, product_id)
        )
        db.commit()
        cur.close()

    @staticmethod
    def delete(product_id):
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        db.commit()
        cur.close()

    @staticmethod
    def update_stock_by_name(product_name, quantity_sold):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "UPDATE products SET stock = stock - %s WHERE product_name = %s",
            (quantity_sold, product_name)
        )
        db.commit()
        cur.close()

    @staticmethod
    def get_for_receipt():
        """Used in receipt form"""
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT product_name, price, stock FROM products")
        products = cur.fetchall()
        cur.close()
        return products