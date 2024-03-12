from flask import Blueprint

from controllers import categories_controller

categories = Blueprint('categories', __name__)


@categories.route('/categories', methods=['POST'])
def create_category():
    return categories_controller.create_category()


@categories.route('/categories', methods=['GET'])
def categories_get_all():
    return categories_controller.categories_get_all()


@categories.route('/categories/<category_id>', methods=['GET'])
def categories_get_by_id(category_id):
    return categories_controller.categories_get_by_id(category_id)


@categories.route('/categories/<category_id>', methods=['PUT'])
def update_categories_name(category_id):
    return categories_controller.update_categories_name(category_id)
