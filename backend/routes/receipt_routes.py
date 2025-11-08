# from flask import render_template, request, redirect, url_for
# from .. import mysql
# from . import receipt_bp
# from flask import render_template, request
# from . import receipt_bp
# import datetime


# -------------------------------------------------
# Create receipt (POS form)
# -------------------------------------------------
# @receipt_bp.route('/products/final', methods=['GET', 'POST'])
# def final_receipt():
#     if request.method == "POST":
#         try:
#             customer_name = request.form['customer_name']
#             product_name = request.form['name']
#             price = float(request.form['price'])
#             stock = int(request.form['stock'])
#             date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             # Create receipt dictionary
#             receipt = {
#                 'customer_name': customer_name,
#                 'name': product_name,
#                 'price': price,
#                 'stock': stock,
#                 'date': date
#             }

#             # Render template with receipt
#             return render_template('receipt.html', receipt=receipt)

#         except Exception as e:
#             return f"Error: {e}"

#     # GET request → show form, no receipt yet
#     return render_template('receipt.html', receipt=None)

# receipt.py (or inside your receipt blueprint module)
from flask import render_template, request
import datetime
from . import receipt_bp  # use the blueprint created in routes/__init__.py

# Route handles both showing the form (GET) and processing it (POST)
@receipt_bp.route('/products/final', methods=['GET', 'POST'])
def final_receipt():
    if request.method == "POST":
        try:
            customer_name = request.form['customer_name']
            product_name = request.form['name']
            price = float(request.form['price'])
            stock = int(request.form['stock'])
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            receipt = {
                'customer_name': customer_name,
                'name': product_name,
                'price': price,
                'stock': stock,
                'date': date
            }

            return render_template('receipt.html', receipt=receipt)

        except Exception as e:
            # For debugging only; in production return a nicer message or flash
            return f"Error: {e}"

    # GET → show form with no receipt
    return render_template('receipt.html', receipt=None)
