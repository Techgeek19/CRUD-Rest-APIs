from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
# python module to deal with file path (to pinpoint where our db file is)

# Init app
app= Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app) 

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rc@localhost/rest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

# Init db
db = SQLAlchemy(app)
# Init ma
ma= Marshmallow(app)    

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Creating a Product
@app.route('/api/product', methods=['POST'])
def add_product():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']
  
  new_product = Product(name, description, price, qty)

  db.session.add(new_product) 
  db.session.commit()

  return product_schema.jsonify(new_product)

#Fetching all products
@app.route('/api/product', methods=['GET'])
def get_products():
    all_products= Product.query.all()
    #dump ==> formatiing python object into json 
    # result = products_schema.dump(all_products)
    # return jsonify(result.data)
    return products_schema.jsonify(all_products)

# Fetching single product
@app.route('/api/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Updating a product
@app.route('/api/product/<id>', methods= ['PUT'])
def update_product(id):
    product= Product.query.get(id)
    name= request.json['name']
    description= request.json['description']
    price= request.json['price']
    qty= request.json['qty']

    product.name= name
    product.description= description
    product.price= price
    product.qty= qty
    db.session.commit()
    return product_schema.jsonify(product)

# Deleting a product
@app.route('/api/product/<id>', methods=['DELETE'])
def delete_product(id):
    product= Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

# Runserver
if __name__=='__main__':
    app.run(debug=True)


