from flask import Blueprint

from controllers import products_categories_xref_controller

xref = Blueprint('products/categories', __name__)


@xref.route('/products/categories', methods=['POST'])
def create_product_category_association():
    return products_categories_xref_controller.create_product_category_association()


@xref.route('/products/categories/<product_id>/<category_id>', methods=['PUT'])
def update_product_category_xref(product_id, category_id):
    return products_categories_xref_controller.update_product_category_xref(product_id, category_id)
