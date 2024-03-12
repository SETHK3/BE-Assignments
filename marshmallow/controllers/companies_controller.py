from flask import jsonify

from db import db
from models.companies import Companies, company_schema, companies_schema
from models.products import Products, product_schema, products_schema
from util.reflection import populate_object


def company_add(req):
    post_data = req.form if req.form else req.json

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    try:
        db.session.add(new_company)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create record'}), 400

    return jsonify({'message': 'company created', 'result': company_schema.dump(new_company)}), 201


def companies_get_all():
    try:
        query = db.session.query(Companies).all()

        if not query:
            return jsonify({'message': 'no companies found'}), 404

        else:
            return jsonify({'message': 'companies found', 'results': companies_schema.dump(query)})
    except:
        return jsonify({'message': 'unable to fetch companies'}), 500


def company_get_by_id(company_id):
    try:
        company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

        return jsonify({'message': f'company found by company_id {company_id}', 'company': company_schema.dump(company_query)}), 200
    except:
        return jsonify({'message': f'no company found with the following id: {company_id}'}), 404


def company_update(req, company_id):
    post_data = req.form if req.form else req.json

    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not query:
        return jsonify({'message': f'company with id {company_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'company updated', 'results': company_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update record'}), 400


def company_delete(company_id):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'error': 'unable to delete record'}), 400

    return jsonify({'message': 'record successfully deleted'}), 200
