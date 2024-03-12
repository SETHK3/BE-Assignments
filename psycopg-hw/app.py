from flask import Flask
import os

from db import create_tables
from routes.products_categories_xref_routes import xref
from routes.categories_routes import categories
from routes.companies_routes import companies
from routes.products_routes import products

app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

app = Flask(__name__)

app.register_blueprint(categories)
app.register_blueprint(companies)
app.register_blueprint(products)
app.register_blueprint(xref)

create_tables()

if __name__ == '__main__':
    app.run(host=app_host, port=app_port)
