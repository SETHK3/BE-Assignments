import os

from flask import jsonify, request
import psycopg2

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_product():
    try:
        post_data = request.form if request.form else request.json

        company_name = post_data.get('company_name')
        price = post_data.get('price')
        description = post_data.get('description')

        if not company_name:
            return jsonify({'message': 'company_name is a required field'}), 400

        cursor.execute("SELECT * FROM products WHERE company_name=%s", [company_name])
        result = cursor.fetchone()
        if result:
            return jsonify({'message': 'product already exists'}), 400

        cursor.execute("INSERT INTO products (company_name, price, description) VALUES(%s, %s, %s)", (company_name, price, description))
        conn.commit()

        return jsonify({'message': f'product {company_name} has been added to the db'}), 201
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


def products_get_all():
    try:
        cursor.execute("SELECT * FROM products;")
        results = cursor.fetchall()

        product_list = []

        for record in results:
            record = {
                'product_id': record[0],
                'company_id': record[1],
                'company_name': record[2],
                'price': record[3],
                'description': record[4],
                'active': record[5]
            }
            product_list.append(record)

        return jsonify({'message': 'products found', 'results': product_list}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error fetching products'}), 500


def active_products_get_all(active=True):
    try:
        cursor.execute("SELECT * FROM products WHERE active=%s", [active])
        results = cursor.fetchall()

        active_list = []

        for record in results:
            record = {
                'product_id': record[0],
                'company_id': record[1],
                'company_name': record[2],
                'price': record[3],
                'description': record[4],
                'active': record[5]
            }
            active_list.append(record)

        return jsonify({'message': 'active products found', 'results': active_list}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error fetching active products'}), 500


def products_by_company_id(company_id):
    try:
        cursor.execute("SELECT * FROM products WHERE company_id=%s", [company_id])
        results = cursor.fetchall()

        products_list = []

        for record in results:
            record = {
                'product_id': record[0],
                'company_id': record[1],
                'company_name': record[2],
                'price': record[3],
                'description': record[4],
                'active': record[5]
            }
            products_list.append(record)

        return jsonify({'message': f'products with company_id {company_id} have been found', 'results': products_list}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': f'error fetching products with the following id: {company_id}'}), 500


def product_get_by_id(product_id):
    try:
        cursor.execute("SELECT * FROM products WHERE product_id=%s", [product_id])
        result = cursor.fetchone()

        if result:
            product_data = {
                'product_id': result[0],
                'company_id': result[1],
                'company_name': result[2],
                'price': result[3],
                'description': result[4],
                'active': result[5]
            }

            return jsonify({'message': f'product with the following id {product_id} has been found', 'results': product_data}), 200
        else:
            return jsonify({'message': f'no product found with the following id: {product_id}'})

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error fetching product with the following id: {product_id}'}), 500


def update_product_price(product_id):
    try:
        post_data = request.form if request.form else request.json

        price = post_data.get('price')

        if not price:
            return jsonify({"message": "price is a required field"}), 400

        cursor.execute("UPDATE products SET price=%s WHERE product_id=%s", (price, product_id))
        conn.commit()

        return jsonify({'message': f'product_id {product_id} price has been successfully updated: {price}'}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': f'error updating price for product_id {product_id}'}), 500


def delete_product(product_id):
    try:
        cursor.execute("SELECT company_id FROM products WHERE product_id=%s", (product_id,))

        cursor.execute("DELETE FROM products_categories_xref WHERE product_id=%s", (product_id,))
        cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        conn.commit()

        return jsonify({'message': f'records with product_id {product_id} have been deleted successfully'}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error deleting records'}), 500
