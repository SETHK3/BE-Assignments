import os

from flask import jsonify, request
import psycopg2

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_category():
    try:
        post_data = request.form if request.form else request.json

        category_name = post_data.get('category_name')

        if not category_name:
            return jsonify({'message': 'category_name is a required field'}), 400

        cursor.execute("SELECT * FROM categories WHERE category_name=%s", [category_name])
        result = cursor.fetchone()
        if result:
            return jsonify({'message': 'category already exists'}), 400

        cursor.execute("INSERT INTO categories (category_name) VALUES(%s)", (category_name,))
        conn.commit()

        return jsonify({'message': f'category {category_name} has been added to the db'}), 201
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


def categories_get_all():
    try:
        cursor.execute("SELECT * FROM categories;")
        results = cursor.fetchall()

        category_list = []

        for record in results:
            record = {
                'category_id': record[0],
                'category_name': record[1]
            }
            category_list.append(record)

        return jsonify({'message': 'categories found', 'results': category_list}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error fetching categories'}), 500


def categories_get_by_id(category_id):
    try:
        cursor.execute("SELECT * FROM categories WHERE category_id=%s", [category_id])
        result = cursor.fetchone()

        category_list = []

        if result:
            category_data = {
                'category_id': result[0],
                'category_name': result[1]
            }
            category_list.append(category_data)

        return jsonify({'message': f'categories with the following id {category_id} have been found', 'results': category_list}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error fetching categories with the following id: {category_id}'}), 500


def update_categories_name(category_id):
    try:
        post_data = request.form if request.form else request.json

        category_name = post_data.get('category_name')

        if not category_name:
            return jsonify({"message": "category_name is a required field"}), 400

        cursor.execute("UPDATE categories SET category_name=%s WHERE category_id=%s", (category_name, category_id))
        conn.commit()

        return jsonify({'message': f'category_id {category_id} name has been successfully updated: {category_name}'}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': f'error updating category_id {category_id}'}), 500
