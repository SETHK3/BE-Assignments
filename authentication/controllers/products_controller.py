from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.products_categories_xref import product_categories_association_table
from models.categories import Categories
from models.products import Products, product_schema, products_schema
from util.reflection import populate_object


@auth_admin
def product_add(req):
    post_data = req.form if req.form else req.json

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    try:
        db.session.add(new_product)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create product'}), 400

    return jsonify({'message': 'product created', 'result': product_schema.dump(new_product)}), 201

@auth
def products_get_all():
    try:
        query = db.session.query(Products).all()

        if not query:
            return jsonify({'message': 'no products found'}), 404

        else:
            return jsonify({'message': 'products found', 'results': products_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'unable to fetch products'}), 500

@auth
def products_get_active():
    try:
        query = db.session.query(Products).filter(Products.active).all()

        return jsonify({'message': 'active products found', 'results': products_schema.dump(query)}), 200
    except:
        return jsonify({'message': 'no active products found'}), 500

@auth
def products_get_by_company_id(company_id):
    try:
        query = db.session.query(Products).filter(Products.company_id == company_id).all()

        return jsonify({'message': f'products found by company_id {company_id}', 'results': products_schema.dump(query)}), 200
    except:
        return jsonify({'message': f'no products found with the following id: {company_id}'}), 404

@auth
def product_get_by_id(product_id):
    try:
        query = db.session.query(Products).filter(Products.product_id == product_id).first()

        return jsonify({'message': f'product found by product_id: {product_id}', 'results': product_schema.dump(query)}), 200
    except:
        return jsonify({'message': f'no product found with the following id: {product_id}'}), 404

@auth_admin
def product_update(req, product_id):
    post_data = req.form if req.form else req.json
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not query:
        return jsonify({'message': f'product with id {product_id} not found'}), 404

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'product updated', 'results': product_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to update record'}), 400

@auth_admin
def product_delete(req, product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    try:
        db.session.delete(product_query)
        db.session.commit()

        return jsonify({'message': f'product with product_id {product_id} was deleted'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': f'product with product_id {product_id} could not be deleted'}), 400

@auth_admin
def product_add_category(req):
    post_data = req.form if req.form else req.json

    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    product_query.categories.append(category_query)

    try:
        db.session.commit()
        return jsonify({'message': 'association created successfully', 'result': product_schema.dump(product_query)}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'error creating association'}), 400

@auth_admin
def product_remove_category(req, product_id, category_id):
    try:
        product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
        category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

        product_query.categories.remove(category_query)

        db.session.commit()

        return jsonify({'message': 'category removed from product successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to remove category'}), 400

