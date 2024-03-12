from flask import Blueprint

from controllers import products_controller

products = Blueprint('products', __name__)


@products.route('/products', methods=['POST'])
def create_product():
    return products_controller.create_product()


@products.route('/products', methods=['GET'])
def products_get_all():
    return products_controller.products_get_all()


@products.route('/products/active', methods=['GET'])
def active_products_get_all():
    return products_controller.active_products_get_all()


@products.route('/products/companies/<company_id>', methods=['GET'])
def products_by_company_id(company_id):
    return products_controller.products_by_company_id(company_id)


@products.route('/products/<product_id>', methods=['GET'])
def product_get_by_id(product_id):
    return products_controller.product_get_by_id(product_id)


@products.route('/products/<product_id>', methods=['PUT'])
def update_product_price(product_id):
    return products_controller.update_product_price(product_id)


@products.route('/products/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    return products_controller.delete_product(product_id)
