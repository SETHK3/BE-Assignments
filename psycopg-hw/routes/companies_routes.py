from flask import Blueprint

from controllers import companies_controller

companies = Blueprint('companies', __name__)


@companies.route('/companies', methods=['POST'])
def create_company():
    return companies_controller.create_company()


@companies.route('/companies', methods=['GET'])
def companies_get_all():
    return companies_controller.companies_get_all()


@companies.route('/companies/<company_id>', methods=['GET'])
def companies_get_by_id(company_id):
    return companies_controller.companies_get_by_id(company_id)


@companies.route('/companies/<company_id>', methods=['PUT'])
def update_companies_name(company_id):
    return companies_controller.update_companies_name(company_id)
