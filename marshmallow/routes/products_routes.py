from flask import Blueprint, request

import controllers

products = Blueprint('products', __name__)


@products.route('/product', methods=['POST'])
def product_add():
    return controllers.product_add(request)


@products.route('/products', methods=['GET'])
def products_get_all():
    return controllers.products_get_all()


@products.route('/products/active', methods=['GET'])
def products_get_active():
    return controllers.products_get_active()


@products.route('/products/company/<company_id>', methods=['GET'])
def products_get_by_company_id(company_id):
    return controllers.products_get_by_company_id(company_id)


@products.route('/product/<product_id>', methods=['GET'])
def product_get_by_id(product_id):
    return controllers.product_get_by_id(product_id)


@products.route('/product/<product_id>', methods=['PUT'])
def product_update(product_id):
    return controllers.product_update(request, product_id)


@products.route('/product/delete/<product_id>', methods=['DELETE'])
def product_delete(product_id):
    return controllers.product_delete(request, product_id)


@products.route('/product/category', methods=['POST'])
def product_add_category():
    return controllers.product_add_category(request)


@products.route('/product/category/<product_id>/<category_id>', methods=['DELETE'])
def product_remove_category(product_id, category_id):
    return controllers.product_remove_category(request, product_id, category_id)
