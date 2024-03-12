from flask import Blueprint, request

import controllers

companies = Blueprint('companies', __name__)


@companies.route('/company', methods=['POST'])
def company_add():
    return controllers.company_add(request)


@companies.route('/companies', methods=['GET'])
def companies_get_all():
    return controllers.companies_get_all()


@companies.route('/company/<company_id>', methods=['GET'])
def company_get_by_id(company_id):
    return controllers.company_get_by_id(company_id)


@companies.route('/company/<company_id>', methods=['PUT'])
def company_update(company_id):
    return controllers.company_update(request, company_id)


@companies.route('/company/delete/<company_id>', methods=['DELETE'])
def company_delete(company_id):
    return controllers.company_delete(company_id)
