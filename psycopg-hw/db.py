import os
import psycopg2

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_tables():
    create_table_companies()
    create_table_products()
    create_table_categories()
    create_table_products_categories_xref()


def create_table_products():
    print("Creating 'products' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            company_id SERIAL REFERENCES companies(company_id),
            company_name VARCHAR NOT NULL,
            price FLOAT,
            description VARCHAR,
            active BOOLEAN DEFAULT TRUE
        );
""")
    conn.commit()


def create_table_companies():
    print("Creating 'companies' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR NOT NULL
        );
""")
    conn.commit()


def create_table_products_categories_xref():
    print("Creating 'products_categories_xref' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products_categories_xref (
                   product_id SERIAL REFERENCES products(product_id),
                   category_id SERIAL REFERENCES categories(category_id)
        );                   
""")
    conn.commit()


def create_table_categories():
    print("Creating 'categories' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
                   category_id SERIAL PRIMARY KEY,
                   category_name VARCHAR NOT NULL
        );
""")
    conn. commit()
