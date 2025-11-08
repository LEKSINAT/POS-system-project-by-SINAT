# routes/auth_routes.py
from flask import render_template, request, redirect, url_for
from .. import mysql   # mysql comes from the app factory
from . import auth_bp
from ..models.product_model import Product


# -------------------------------------------------
# Registration form (home page)
# -------------------------------------------------
@auth_bp.route('/', methods=['GET'])
def home():
    try:
        products = Product.all()
        total_products = len(products)
        # products rows: [product_id, product_name, price, stock]
        total_stock = sum((p[3] or 0) for p in products)
    except Exception:
        total_products = 0
        total_stock = 0

    # No chat implemented yet; placeholder
    total_messages = 0

    return render_template(
        'index.html',
        total_products=total_products,
        total_stock=total_stock,
        total_messages=total_messages,
    )


# -------------------------------------------------
# Register new user
# -------------------------------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    name     = request.form['name']
    email    = request.form['email']
    password = request.form['password']

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('auth.home'))
    except Exception as e:
        return f"Error: {e}"


# -------------------------------------------------
# Login form
# -------------------------------------------------
@auth_bp.route('/login_form')
def login_form():
    return render_template('login_form.html')


# -------------------------------------------------
# Login handling
# -------------------------------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    name     = request.form['name']
    email    = request.form['email']
    password = request.form['password']

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM users WHERE email = %s AND name = %s AND password = %s',
            (email, name, password)
        )
        user = cur.fetchone()
        cur.close()

        if user:
            return redirect(url_for('auth.home'))
        return 'Invalid login details. Please try again.'
    except Exception as e:
        return f"Error: {e}"