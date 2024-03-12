from flask import jsonify

from db import db
from models.companies import Companies


def company_add(req):
    post_data = req.form if req.form else req.json

    fields = ['company_name']
    required_fields = ['company_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({'message': f'{field} is required'}), 400

        values[field] = field_data

    new_company = Companies(values['company_name'])

    try:
        db.session.add(new_company)
        db.session.commit()
        company_id = new_company.company_id
        values['company_id'] = company_id

        return jsonify({'message': 'company created', 'result': values}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create record'}), 400


def companies_get_all():
    try:
        query = db.session.query(Companies).all()

        records_list = []

        for record in query:
            record_dict = {
                'company_id': record.company_id,
                'company_name': record.company_name,
            }

            records_list.append(record_dict)

        return jsonify({'message': 'companies found', 'results': records_list}), 200
    except:
        return jsonify({'message': 'unable to fetch companies'}), 500


def company_by_id(company_id):
    try:
        query = db.session.query(Companies).filter(Companies.company_id == company_id).all()

        records_list = []

        for company in query:
            record_dict = {
                'company_id': company.company_id,
                'company_name': company.company_name
            }

            records_list.append(record_dict)

        return jsonify({'message': f'company found by company_id {company_id}', 'results': records_list}), 200
    except:
        return jsonify({'message': f'no company found with the following id: {company_id}'}), 500


def company_update(req, company_id):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not query:
        return jsonify({'message': f'company with id {company_id} not found'}), 404

    update_data = req.form if req.form else req.json

    query.company_name = update_data.get('company_name', query.company_name)

    try:
        db.session.commit()
        return jsonify({'message': 'product updated', 'results': {
            'company_id': query.company_id,
            'company_name': query.company_name
        }}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update record'}), 400
