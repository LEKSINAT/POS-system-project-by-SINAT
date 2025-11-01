from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# -----------------------
# MySQL configuration
# -----------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'        # change if needed
app.config['MYSQL_PASSWORD'] = ''        # change if needed
app.config['MYSQL_DB'] = 'product'       # your database name

mysql = MySQL(app)

# Serve images from the top-level `img/` folder (so you don't have to move files)
@app.route('/img/<path:filename>')
def serve_img(filename):
    # app.root_path is the project folder; img/ lives at the repository root
    img_dir = os.path.join(app.root_path, 'img')
    return send_from_directory(img_dir, filename)

# -----------------------
# Home page
# -----------------------
@app.route('/')
def home():
    return render_template('index.html')  # your registration form

# -----------------------
# Handle registration
# -----------------------
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error: {e}"

# -----------------------
# List products
# -----------------------
@app.route('/products')
def product_list():
    # try:
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('category.html', products=products)
    # except Exception as e:
    #     return f"Error: {e}"

# -----------------------
# Login form route
# -----------------------
@app.route('/login_form')
def login_form():
    return render_template('login_form.html')

# -----------------------
# Handle login
# -----------------------
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    try:
        cur = mysql.connection.cursor()
        # Print the values for debugging
        print(f"Trying to login with: name={name}, email={email}, password={password}")
        
        cur.execute('SELECT * FROM users WHERE email = %s AND name = %s AND password = %s', 
                   (email, name, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            print("Login successful!")
            return redirect(url_for('home'))
        else:
            print("Login failed - no matching user found")
            return 'Invalid login details. Please try again.'
    except Exception as e:
        return f"Error: {e}"

# -----------------------
# Edit product route
# -----------------------
@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            name = request.form['name']
            price = request.form['price']
            stock = request.form['stock']
            
            cur.execute("""
                UPDATE products 
                SET product_name = %s, price = %s, stock = %s 
                WHERE product_id = %s
                """, (name, price, stock, product_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('product_list'))
        
        # GET request - show edit form
        cur.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
        product = cur.fetchone()
        cur.close()
        if product:
            return render_template('edit.html', product=product)
        else:
            return 'Product not found.'
            
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------
# Add product route
# -----------------------
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = request.form['price']
            stock = request.form['stock']
            
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO products (product_name, price, stock)
                VALUES (%s, %s, %s)
            """, (name, price, stock))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('product_list'))
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Show the add product form
    return render_template('add.html')

# -----------------------
# Delete product route
# -----------------------
@app.route('/products/delete/<int:product_id>')
def delete_product(product_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM products WHERE product_id = %s', (product_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('product_list'))
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------
# Receipt routes
# -----------------------
@app.route('/receipt/new', methods=['GET', 'POST'])
def create_receipt():
    if request.method == 'POST':
        try:
            # Get the cart items from the form
            items = request.form.getlist('items[]')
            quantities = request.form.getlist('quantities[]')
            prices = request.form.getlist('prices[]')
            
            cur = mysql.connection.cursor()
            
            # Create receipt header
            cur.execute("""
                INSERT INTO receipts (date, cashier_name, total_amount)
                VALUES (NOW(), %s, 0)
            """, (request.form.get('cashier_name', 'Default Cashier'),))
            
            receipt_id = cur.lastrowid
            total_amount = 0
            
            # Add receipt items
            for item, qty, price in zip(items, quantities, prices):
                qty = int(qty)
                price = float(price)
                amount = qty * price
                total_amount += amount
                
                cur.execute("""
                    INSERT INTO receipt_items (receipt_id, product_name, quantity, price, amount)
                    VALUES (%s, %s, %s, %s, %s)
                """, (receipt_id, item, qty, price, amount))
                
                # Update stock
                cur.execute("""
                    UPDATE products 
                    SET stock = stock - %s 
                    WHERE product_name = %s
                """, (qty, item))
            
            # Update receipt total
            cur.execute("UPDATE receipts SET total_amount = %s WHERE id = %s", 
                       (total_amount, receipt_id))
            
            mysql.connection.commit()
            cur.close()
            
            # Redirect to view the receipt
            return redirect(url_for('view_receipt', receipt_id=receipt_id))
            
        except Exception as e:
            return f"Error creating receipt: {str(e)}"
            
    # GET request - show receipt form
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name, price, stock FROM products")
    products = cur.fetchall()
    cur.close()
    
    return render_template('create_receipt.html', products=products)

@app.route('/receipt/<int:receipt_id>')
def view_receipt(receipt_id):
    try:
        cur = mysql.connection.cursor()
        
        # Get receipt header
        cur.execute("""
            SELECT id, date, cashier_name, total_amount 
            FROM receipts 
            WHERE id = %s
        """, (receipt_id,))
        receipt = cur.fetchone()
        
        if not receipt:
            return "Receipt not found", 404
            
        # Get receipt items
        cur.execute("""
            SELECT product_name, quantity, price, amount 
            FROM receipt_items 
            WHERE receipt_id = %s
        """, (receipt_id,))
        items = cur.fetchall()
        
        cur.close()
        
        return render_template('receipt.html',
                            receipt_number=receipt[0],
                            date=receipt[1].strftime('%Y-%m-%d'),
                            time=receipt[1].strftime('%H:%M:%S'),
                            cashier_name=receipt[2],
                            total=receipt[3],
                            items=items)
                            
    except Exception as e:
        return f"Error viewing receipt: {str(e)}"

# -----------------------
# Run the app
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
 
    
    
    
    
#     from flask import Flask, render_template
# import os

# template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# app = Flask(__name__, template_folder=template_dir)

# @app.route('/')
# def home():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
# <a href="{{ url_for('delete_product', product_id=product[0]) }}">Delete</a>
