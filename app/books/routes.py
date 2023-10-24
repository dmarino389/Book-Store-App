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
def handle_create_book():
    body = request.json

    if body is None:
        response = {
            "message": "You need to add a book."
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


from flask_jwt_extended import create_access_token
from flask import request, make_response
from ..models import User
from datetime import timedelta


#This allows the user to delete a current users book
from flask_jwt_extended import jwt_required, current_user
from ..models import Book

@books.delete("/delete/<book_id>")
@jwt_required()
def handle_delete_book(book_id):
    book = Book.query.filter_by(id=book_id).one_or_none()
    if book is None:
        response = {
            "message": "Book does not exist"
        }
        return response, 404

    if book.created_by != current_user.id:
        response = {
            "message":"you cant delete someone elses entry"
        }
        return response, 401
    
    book.delete()

    response = {
        "message": f"Book {book.id} deleted"
    }
    return response, 200


# This code block allows for the book to be updated  
@books.put("/update/book/<book_id>")
@jwt_required()
def handle_update_book(book_id):
    body = request.json

    book = Book.query.filter_by(id=book_id).one_or_none()
    if book is None:
        response = {
            "message": "not found"
        }
        return response, 404

    if book.created_by != current_user.id:
        response = {"message":"no sir/maam. This doesnt seem to be yours."}
        return response, 401
    

    book.title = body.get("title", book.title)
    book.description = body.get("description", book.description)
    
    book.update()

    response = {
        "message": "quiz updated",
        "quiz": book.to_response()
    }
    return response, 200