from flask import Blueprint

from controllers import products_controller

product = Blueprint('product', __name__)


@product.route('/product', methods=['POST'])
def create_product():
    return products_controller.create_product()


@product.route('/products', methods=['GET'])
def read_all_products():
    return products_controller.read_all_products()


@product.route('/products/active', methods=['GET'])
def read_active_products():
    return products_controller.read_active_products()


@product.route('/product/<product_id>', methods=['GET'])
def read_product_by_id(product_id):
    return products_controller.read_product_by_id(product_id)


@product.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    return products_controller.update_product(product_id)


@product.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    return products_controller.delete_product(product_id)
