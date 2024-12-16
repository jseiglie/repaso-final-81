"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Books, Authors, Categories, Books_Categories
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/user/register', methods=['POST'])
def register():
    email = request.json.get('email', None) 
    password =  request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": "missing data"}), 400
    user = User.query.filter_by(email = email).first()
    if user:
        return jsonify({"msg": "email taken"}), 400
    hashed = generate_password_hash(password)
    new_user = User(email=email, password=hashed, is_active=True)
    db.session.add(new_user)
    db.session.commit()
    token = create_access_token(identity=str(new_user.id))
    return jsonify({"msg": "OK", "token": token}), 201

    
@api.route('/user/login', methods=['POST'])
def login():
    email = request.json.get('email', None) 
    password =  request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": "missing data"}), 400
    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"msg": "no account with this email"}), 404
    
    if not check_password_hash(user.password, password):
        return jsonify({"msg": "email/password wrong"}), 400
    
    token = create_access_token(identity=str(user.id))
    return jsonify({"msg": "OK", "token": token, "user": user.serialize()}), 200

#CRUD

@api.route('/books', methods=['GET'])
def all_books():
    books = Books.query.all() # devuelve lista
    books = [book.serialize() for book in books]
    return jsonify({"msg": 'ok', 'books': books})

@api.route('/books/<int:id>', methods=['GET'])
def one_book(id):
    book = Books.query.get(id) # devuelve objeto
    return jsonify({"msg": 'ok', 'books': book.serialize()})

@api.route('/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Books.query.get(id) # devuelve objeto\
    db.session.delete(book)
    db.session.commit()
    return jsonify({"msg": 'book deleted', 'books': book.serialize()})



@api.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    title = request.json.get('title', None)
    author_id = request.json.get('author_id', None)
    if title is None or author_id is None: 
        return jsonify({"msg": 'missing data'})
    new_book = Books(title=title, author_id=author_id)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"msg": 'ok', "books": new_book.serialize()})

@api.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def edit_book(id):
    title = request.json.get('title', None)
    author_id = request.json.get('author_id', None)
    
    book = Books.query.get(id) # devuelve objeto
  
    if title:
        book.title= title

    book.author_id = author_id or book.author_id

    db.session.commit()
    return jsonify({"msg": 'ok', "books": book.serialize()})



@api.route('/get_user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    id = get_jwt_identity()
    user = User.query.get(id)
    return jsonify({"msg": "ok", "user": user.serialize()})
