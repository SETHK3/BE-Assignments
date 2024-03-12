import os

from flask import jsonify, request
import psycopg2

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_product_category_association():
    try:
        post_data = request.form if request.form else request.json

        product_id = post_data.get('product_id')
        category_id = post_data.get('category_id')

        if not product_id or not category_id:
            return jsonify({'message': 'both product_id and category_id are required fields'}), 400

        cursor.execute("INSERT INTO products_categories_xref (product_id, category_id) VALUES(%s, %s)", (product_id, category_id))
        conn.commit()

        return jsonify({'message': 'association created successfully'}), 201

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error creating association'}), 500


def update_product_category_xref(product_id, category_id):
    try:
        update_data = request.form if request.form else request.json

        product_id = update_data.get('product_id')
        category_id = update_data.get('category_id')

        cursor.execute("UPDATE products_categories_xref SET product_id=%s, category_id=%s WHERE product_id=%s AND category_id=%s", (product_id, category_id))
        conn.commit()

        return jsonify({'message': 'record updated successfully'}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error updating record'}), 500
