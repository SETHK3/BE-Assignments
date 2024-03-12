from flask import jsonify, request

from data import product_records


def create_product():
    data = request.form if request.form else request.json

    product = {}

    product['product_id'] = data['product_id']
    product['product_name'] = data['product_name']
    product['description'] = data['description']
    product['price'] = data['price']
    product['active'] = data['active']

    product_records.append(product)

    return jsonify({'message': 'product added', 'results': product}), 201


def read_all_products():
    return jsonify({'message': 'products found', 'results': product_records}), 200


def read_active_products():
    active_products = []

    for product in product_records:
        if product['active'] == True:
            active_products.append(product)

    if active_products:
        return jsonify({'message': 'active products found', 'results': active_products}), 200
    else:
        return jsonify({'message': 'no active products found'}), 404


def read_product_by_id(product_id):
    for product in product_records:
        if product['product_id'] == int(product_id):
            return jsonify({'message': 'product found', 'results': product}), 200

    return jsonify({'message': f'product with id {product_id} not found'}), 404


def update_product(product_id):
    data = request.form if request.form else request.json

    product = {}

    for record in product_records:
        if record['product_id'] == int(product_id):
            product = record

    product['product_name'] = data.get('product_name', product['product_name'])
    product['description'] = data.get('description', product['description'])
    product['price'] = data.get('price', product['price'])
    product['active'] = data.get('active', product['active'])

    return jsonify({'message': 'product updated', 'results': product}), 200


def delete_product(product_id):
    for product in product_records:
        if product['product_id'] == int(product_id):
            product_records.remove(product)
            return jsonify({'message': f'product with id {product_id} has been deleted'}), 200
