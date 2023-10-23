from flask import Flask, jsonify, request
from ..models import db, User, Book
from app import app
from . import books_blueprint as books



@books.route('/api/search/book', methods=['GET'])
def search_book():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    books = Book.query.filter(Book.title.ilike(f'%{title}%')).all()
    return jsonify([book.to_response() for book in books])

# @books.route('/api/search/author', methods=['GET'])
# def search_author():
#     name = request.args.get('name')
#     if not name:
#         return jsonify({'error': 'Name is required'}), 400

#     authors = Author.query.filter(
#         (Author.first_name.ilike(f'%{name}%')) |
#         (Author.last_name.ilike(f'%{name}%'))
#     ).all()

#     return jsonify([author.to_response() for author in authors])




@books.post("/new")
def handle_register():
    body = request.json

    if body is None:
        response = {
            "message": "username and password are required to register"
        }
        return response, 400

    username = body.get("username")
    if username is None:
        response = {
            "message": "username is required"
        }
        return response, 400

    password = body.get("password")
    if password is None:
        response = {
            "message": "password is required"
        }
        return response, 400

    existing_user = User.query.filter_by(username=username).one_or_none()
    if existing_user is not None:
        response = {
            "message": "username already in use"
        }
        return response, 400
    
    user = User(username=username, password=password)
    user.create()

    response = {
        "message": "user registered",
        "data": user.to_response()
    }
    return response, 201

from . import auth_blueprint as auth
from flask_jwt_extended import create_access_token
from flask import request, make_response
from ..models import User
from datetime import timedelta

@auth.post("/register")
def handle_register():
    body = request.json

    if body is None:
        response = {
            "message": "username and password are required to register"
        }
        return response, 400

    username = body.get("username")
    if username is None:
        response = {
            "message": "username is required"
        }
        return response, 400

    password = body.get("password")
    if password is None:
        response = {
            "message": "password is required"
        }
        return response, 400

    existing_user = User.query.filter_by(username=username).one_or_none()
    if existing_user is not None:
        response = {
            "message": "username already in use"
        }
        return response, 400
    
    user = User(username=username, password=password)
    user.create()

    response = {
        "message": "user registered",
        "data": user.to_response()
    }
    return response, 201


from flask_jwt_extended import jwt_required, current_user
from ..models import Book

@books.delete("/delete/<book_id>")
@jwt_required()
def handle_delete_quiz(book_id):
    book = Book.query.filter_by(id=book_id).one_or_none()
    if book is None:
        response = {
            "message": "quiz does not exist"
        }
        return response, 404

    if book.created_by != current_user.id:
        response = {
            "message":"you cant delete someone elses quiz"
        }
        return response, 401
    
    book.delete()

    response = {
        "message": f"quiz {book.id} deleted"
    }
    return response, 200