# from flask import Flask, render_template, request, redirect, url_for
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# # -----------------------
# # MySQL configuration
# # -----------------------
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'        # change if needed
# app.config['MYSQL_PASSWORD'] = ''        # change if needed
# app.config['MYSQL_DB'] = 'product'       # your database name

# mysql = MySQL(app)

# # -----------------------
# # Home page
# # -----------------------
# @app.route('/')
# def home():
#     return render_template('index.html')  # your registration form

# # -----------------------
# # Handle registration
# # -----------------------
# @app.route('/register', methods=['POST'])
# def register():
#     name = request.form['name']
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         cur = mysql.connection.cursor()
#         cur.execute(
#             "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
#             (name, email, password)
#         )
#         mysql.connection.commit()
#         cur.close()
#         return redirect(url_for('home'))
#     except Exception as e:
#         return f"Error: {e}"

# # -----------------------
# # List products
# # -----------------------
# @app.route('/products')
# def product_list():
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM products")
#         products = cur.fetchall()
#         cur.close()
#         return render_template('category.html', products=products)
#     except Exception as e:
#         return f"Error: {e}"

# # -----------------------
# # Run the app
# # -----------------------
# if __name__ == '__main__':
#     app.run(debug=True)
 
    
    
    
# #     from flask import Flask, render_template
# # import os

# # template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# # app = Flask(__name__, template_folder=template_dir)

# # @app.route('/')
# # def home():
# #     return render_template('index.html')

# # if __name__ == '__main__':
# #     app.run(debug=True)
# # <a href="{{ url_for('delete_product', product_id=product[0]) }}">Delete</a>
