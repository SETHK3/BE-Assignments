from flask import jsonify

from db import db
from models.categories import Categories, category_schema, categories_schema
from models.products import Products, product_schema, products_schema
from util.reflection import populate_object


def category_add(req):
    post_data = req.form if req.form else req.json

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create category'}), 400

    return jsonify({'message': 'category created', 'result': category_schema.dump(new_category)}), 201


def categories_get_all():
    try:
        query = db.session.query(Categories).all()

        if not query:
            return jsonify({'message': 'no categories found'}), 404

        return jsonify({'message': 'categories found', 'results': categories_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'unable to fetch categories'}), 500


def category_get_by_id(category_id):
    try:
        category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

        if category_query:
            products = [product_schema.dump(product) for product in category_query.products]

        return jsonify({'message': f'category found by category_id: {category_id}', 'category': category_schema.dump(category_query), 'products': products}), 200
    except:
        return jsonify({'message': f'no category found with the following id: {category_id}'}), 500


def category_update(req, category_id):
    post_data = req.form if req.form else req.json

    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not query:
        return jsonify({'message': f'category with id {category_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'category updated', 'results': category_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update record'}), 400


def category_delete(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'error': 'unable to delete record'}), 400

    return jsonify({'message': 'record successfully deleted'}), 200
