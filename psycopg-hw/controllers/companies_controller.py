import os

from flask import jsonify, request
import psycopg2

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_company():
    try:
        post_data = request.form if request.form else request.json

        company_name = post_data.get('company_name')

        if not company_name:
            return jsonify({"message": "company_name is a required field"}), 400

        cursor.execute("SELECT * FROM companies WHERE company_name=%s", [company_name])
        result = cursor.fetchone()
        if result:
            return jsonify({"message": "company already exists"}), 400

        cursor.execute("INSERT INTO companies (company_name) VALUES(%s)", (company_name,))
        conn.commit()

        return jsonify({"message": f'company {company_name} has been added to the db'}), 201
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


def companies_get_all():
    try:
        cursor.execute("SELECT * FROM companies;")
        results = cursor.fetchall()

        company_list = []

        for record in results:
            record = {
                'company_id': record[0],
                'company_name': record[1]
            }
            company_list.append(record)

        return jsonify({'message': 'companies found', 'results': company_list}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': 'error fetching companies'}), 500


def companies_get_by_id(company_id):
    try:
        cursor.execute("SELECT * FROM companies WHERE company_id=%s", [company_id])
        result = cursor.fetchone()

        company_list = []

        if result:
            company_data = {
                'company_id': result[0],
                'company_name': result[1]
            }
            company_list.append(company_data)

        return jsonify({'message': f'companies with company_id {company_id} have been found', 'results': company_list}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': f'error fetching companies with the following id: {company_id}'}), 500


def update_companies_name(company_id):
    try:
        post_data = request.form if request.form else request.json

        company_name = post_data.get('company_name')

        if not company_name:
            return jsonify({"message": "company_name is a required field"}), 400

        cursor.execute("UPDATE companies SET company_name=%s WHERE company_id=%s", (company_name, company_id))
        conn.commit()

        return jsonify({'message': f'company_id {company_id} name has been successfully updated: {company_name}'}), 200

    except Exception:
        cursor.rollback()
        return jsonify({'message': f'error updating company_id {company_id}'}), 500
