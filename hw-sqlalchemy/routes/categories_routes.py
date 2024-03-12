from flask import Blueprint, request

from controllers import categories_controller

categories = Blueprint('categories', __name__)


@categories.route('/category', methods=['POST'])
def category_add():
    return categories_controller.category_add(request)


@categories.route('/categories', methods=['GET'])
def categories_get_all():
    return categories_controller.categories_get_all()


@categories.route('/category/<category_id>', methods=['GET'])
def category_by_id(category_id):
    return categories_controller.category_by_id(category_id)


@categories.route('/category/<category_id>', methods=['PUT'])
def category_update(category_id):
    return categories_controller.category_update(request, category_id)
