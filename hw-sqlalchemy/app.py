from flask import Flask, jsonify, request
import psycopg2
import os

from db import *
from models.categories import Categories
from models.companies import Companies
from models.products import Products
from routes.categories_routes import categories
from routes.companies_routes import companies
from routes.products_routes import products

flask_host = os.environ.get('FLASK_HOST')
flask_port = os.environ.get('FLASK_PORT')

database_scheme = os.environ.get('DATABASE_SCHEME')
database_user = os.environ.get('DATABASE_USER')
database_address = os.environ.get('DATABASE_ADDRESS')
database_port = os.environ.get('DATABASE_PORT')
database_name = os.environ.get('DATABASE_NAME')

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_scheme}{database_user}@{database_address}:{database_port}/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)

app.register_blueprint(categories)
app.register_blueprint(companies)
app.register_blueprint(products)


def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully")


if __name__ == '__main__':
    create_tables()
    app.run(host=flask_host, port=flask_port)
