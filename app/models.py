from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):  # This represents both a user and an author in this context
    id = db.Column(db.String(64), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    books = db.relationship('Book', backref='author', lazy='dynamic', cascade = 'all,delete')

    def __init__(self, username, password):
        self.id = str(uuid4())
        self.username = username
        self.password = generate_password_hash(password)

    def compare_password(self, password):
        return check_password_hash(self.password, password)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "password":
                setattr(self, key, generate_password_hash(value))
            else:
                setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "username": self.username,
            # Convert the books relationship into a list of dictionaries representing books
            "books": [book.to_response() for book in self.books.all()]
        }


class Book(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(64), db.ForeignKey("user.id"), nullable=False)  # Assuming 'user.id' refers to authors

    def __init__(self, title, description, author):
        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.author = author  # Set the author (User object)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "author": self.author.to_response()  # This will embed the author's information
        }
