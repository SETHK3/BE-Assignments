import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.companies import Companies, CompaniesSchema
from models.products_categories_xref import product_categories_association_table


class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    price = db.Column(db.Float(), nullable=False)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Companies.company_id", ondelete="CASCADE"), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    company = db.relationship("Companies", foreign_keys='[Products.company_id]', back_populates='products')
    categories = db.relationship("Categories", secondary=product_categories_association_table, back_populates='products')

    def __init__(self, product_name, description, price, company_id, active):
        self.product_name = product_name
        self.description = description
        self.price = price
        self.company_id = company_id
        self.active = active

    def new_product_obj():
        return Products("", "", 0, "", True)


class ProductsSchema(ma.Schema):
    class Meta:
        fields = ['product_id', 'product_name', 'description', 'price', 'company', 'categories', 'active']
    company = ma.fields.Nested("CompaniesSchema", exclude=['products'])
    categories = ma.fields.Nested("CategoriesSchema", many=True, exclude=['products'])


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)


class ProductNameIDSchema(ma.Schema):
    class Meta:
        fields = ['product_id', 'product_name', 'price']


product_name_id_schema = ProductNameIDSchema()
products_name_id_schema = ProductNameIDSchema(many=True)
