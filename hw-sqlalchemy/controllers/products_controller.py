from flask import jsonify

from db import db

from models.products_categories_xref import product_categories_association_table
from models.categories import Categories
from models.products import Products


def product_add(req):
    post_data = req.form if req.form else req.json

    fields = ['product_name', 'description', 'price', 'company_id']
    required_fields = ['product_name', 'description', 'price', 'company_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field:
            return jsonify({'message': f'{field} is required'}), 400

        values[field] = field_data

    new_product = Products(**values)

    try:
        db.session.add(new_product)
        db.session.commit()
        product_id = new_product.product_id
        values['product_id'] = product_id
        return jsonify({'message': 'product created', 'result': values}), 201

    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create product'}), 400


def products_get_all():
    try:
        query = db.session.query(Products).all()

        records_list = []

        for product in query:
            categories_list = []
            for category in product.categories:
                categories_list.append({
                    'category_id': category.category_id,
                    'category_name': category.category_name
                })

            record_dict = {
                'product_id': product.product_id,
                'product_name': product.product_name,
                'description': product.description,
                'price': product.price,
                'company': {
                    'company_id': product.company.company_id,
                    'company_name': product.company.company_name
                },
                'categories': categories_list,
                'active': product.active
            }

            records_list.append(record_dict)

        return jsonify({'message': 'products found', 'results': records_list}), 200
    except:
        return jsonify({'message': 'unable to fetch products'}), 500


def products_get_active():
    try:
        query = db.session.query(Products).filter(Products.active).all()

        records_list = []

        for product in query:
            record_dict = {
                'product_id': product.product_id,
                'product_name': product.product_name,
                'active': product.active
            }

            records_list.append(record_dict)

        return jsonify({'message': 'active products found', 'results': records_list}), 200
    except:
        return jsonify({'message': 'no active products found'}), 500


def products_by_company_id(company_id):
    try:
        query = db.session.query(Products).filter(Products.company_id == company_id).all()

        records_list = []

        for product in query:
            record_dict = {
                'product_id': product.product_id,
                'product_name': product.product_name
            }

            records_list.append(record_dict)

        return jsonify({'message': f'products found by company_id {company_id}', 'results': records_list}), 200
    except:
        return jsonify({'message': f'no products found with the following id: {company_id}'}), 500


def product_by_id(product_id):
    try:
        query = db.session.query(Products).filter(Products.product_id == product_id).all()

        records_list = []

        for product in query:
            record_dict = {
                'product_id': product.product_id,
                'product_name': product.product_name
            }

            records_list.append(record_dict)

        return jsonify({'message': f'product found by product_id: {product_id}', 'results': records_list}), 200
    except:
        return jsonify({'message': f'no product found with the following id: {product_id}'}), 500


def product_update(req, product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not query:
        return jsonify({'message': f'product with id {product_id} not found'}), 404

    update_data = req.form if req.form else req.json

    query.product_name = update_data.get('product_name', query.product_name)
    query.description = update_data.get('description', query.description)
    query.price = update_data.get('price', query.price)
    query.company_id = update_data.get('company_id', query.company_id)
    query.active = update_data.get('active', query.active)

    try:
        db.session.commit()
        return jsonify({'message': 'product updated', 'results': {
            'product_id': query.product_id,
            'product_name': query.product_name,
            'description': query.description,
            'price': query.price,
            'company_id': query.company_id,
            'active': query.active
        }}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update record'}), 400


def product_delete(req, product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    try:
        db.session.delete(product_query)
        db.session.commit()

        return jsonify({'message': f'product with product_id {product_id} was deleted'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': f'product with product_id {product_id} could not be deleted'}), 400


def product_add_category(req, values):
    post_data = req.form if req.form else req.json

    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == values['product_id']).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == values['category_id']).first()

    if not product_query or not category_query:
        return jsonify({'message': 'product or category not found'}), 404

    else:
        product_query.categories.append(category_query)

    try:
        db.session.commit()
        return jsonify({'message': 'association created successfully'}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'error creating association'}), 400


def product_remove_category(req, product_id, category_id):
    try:
        product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
        category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

        if not product_query or not category_query:
            return jsonify({'message': 'Product or category not found'}), 404

        product_query.categories.remove(category_query)

        db.session.commit()

        return jsonify({'message': 'category removed from product successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to remove category'}), 400
