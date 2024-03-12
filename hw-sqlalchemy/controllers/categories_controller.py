from flask import jsonify

from db import db
from models.categories import Categories


def category_add(req):
    post_data = req.form if req.form else req.json

    fields = ['category_name']
    required_fields = ['category_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({'message': f'{field} is required'}), 400

        values[field] = field_data

    new_category = Categories(values['category_name'])

    try:
        db.session.add(new_category)
        db.session.commit()
        category_id = new_category.category_id
        values['category_id'] = category_id

        return jsonify({'message': 'category created', 'result': values}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create record'}), 400


def categories_get_all():
    try:
        query = db.session.query(Categories).all()

        records_list = []

        for record in query:
            record_dict = {
                'category_id': record.category_id,
                'category_name': record.category_name,
            }

            records_list.append(record_dict)

        return jsonify({'message': 'categories found', 'results': records_list}), 200
    except:
        return jsonify({'message': 'unable to fetch categories'}), 500


def category_by_id(category_id):
    try:
        query = db.session.query(Categories).filter(Categories.category_id == category_id).all()

        records_list = []

        for category in query:
            record_dict = {
                'category_id': category.category_id,
                'category_name': category.category_name
            }

            records_list.append(record_dict)

        return jsonify({'message': f'category found by category_id: {category_id}', 'results': records_list}), 200
    except:
        return jsonify({'message': f'no category found with the following id: {category_id}'}), 500


def category_update(req, category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not query:
        return jsonify({'message': f'category with id {category_id} not found'}), 404

    update_data = req.form if req.form else req.json

    query.category_name = update_data.get('category_name', query.category_name)

    try:
        db.session.commit()
        return jsonify({'message': 'category updated', 'results': {
            'category_id': query.category_id,
            'category_name': query.category_name
        }}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update record'}), 400
