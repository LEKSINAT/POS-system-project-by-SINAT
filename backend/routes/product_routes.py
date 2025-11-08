# routes/product_routes.py
from flask import (
    render_template, request, redirect, url_for,
    send_from_directory, current_app, flash, abort, Response
)
from . import product_bp
from ..models.product_model import Product
import os
import csv
import io


# ── Serve images from top-level img/ folder ───────
@product_bp.route('/img/<path:filename>')
def serve_img(filename):
    img_dir = os.path.join(current_app.root_path, 'frontend', 'img')
    return send_from_directory(img_dir, filename)


# ── List all products ─────────────────────────────
@product_bp.route('/products')
def product_list():
    q = request.args.get('search', '').strip()
    try:
        products = Product.search_by_name(q) if q else Product.all()
    except Exception as e:
        products = []
        flash(f"Database error while loading products: {e}", 'error')
    dl = request.args.get('download', '').strip().lower()
    if dl == 'excel':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['NB', 'NAME', 'PRICE', 'STOCK'])
        for idx, p in enumerate(products, start=1):
            writer.writerow([idx, p[1], f"{p[2]:.2f}", p[3]])
        csv_data = output.getvalue()
        output.close()
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=products.csv'}
        )
    
    return render_template('category.html', products=products)


# ── Add product (GET → form, POST → save) ─────────
@product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            name  = request.form['name'].strip()
            price = float(request.form['price'])
            stock = int(request.form['stock'])

            if not name:
                flash('Product name is required.', 'error')
            elif price < 0:
                flash('Price cannot be negative.', 'error')
            elif stock < 0:
                flash('Stock cannot be negative.', 'error')
            else:
                Product.create(name, price, stock)
                flash('Product added successfully!', 'success')
                return redirect(url_for('product.product_list'))
        except (ValueError, KeyError):
            flash('Invalid input. Check price/stock values.', 'error')

    return render_template('add.html')


# ── Edit product ───────────────────────────────────
@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.find(product_id)
    if not product:
        abort(404, description="Product not found.")

    if request.method == 'POST':
        try:
            name  = request.form['name'].strip()
            price = float(request.form['price'])
            stock = int(request.form['stock'])

            if not name:
                flash('Product name is required.', 'error')
            elif price < 0 or stock < 0:
                flash('Price and stock must be non-negative.', 'error')
            else:
                Product.update(product_id, name, price, stock)
                flash('Product updated!', 'success')
                return redirect(url_for('product.product_list'))
        except (ValueError, KeyError):
            flash('Invalid input.', 'error')

    return render_template('edit.html', product=product)


# ── Delete product ─────────────────────────────────
@product_bp.route('/delete/<int:product_id>')
def delete_product(product_id):
    if Product.find(product_id):
        Product.delete(product_id)
        flash('Product deleted.', 'success')
    else:
        flash('Product not found.', 'error')
    return redirect(url_for('product.product_list'))


# ── Sales page (card layout) ───────────────────────
@product_bp.route('/sale')
def sale():
    try:
        products = Product.all()
    except Exception:
        products = []
    return render_template('sale.html', products=products)