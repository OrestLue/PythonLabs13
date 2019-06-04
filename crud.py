from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=False)
    author = db.Column(db.String(40), unique=False)
    publishing_house = db.Column(db.String(40), unique=False)
    price = db.Column(db.FLOAT, unique=False)
    ean13 = db.Column(db.BIGINT, unique=False)
    isbn = db.Column(db.String(17), unique=False)
    description = db.Column(db.String(80), unique=False)

    def __init__(self, title, author, publishing_house, price, ean13, isbn, description):
        self.title = title
        self.author = author
        self.publishing_house = publishing_house
        self.price = price
        self.ean13 = ean13
        self.isbn = isbn
        self.description = description


class BookSchema(ma.Schema):
    class Meta:
        fields = ('title', 'author', 'publishing_house', 'price', 'ean13', 'isbn', 'description')
        db.create_all()


book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route("/book", methods=["POST"])
def add_user():
    title = request.json['title']
    author = request.json['author']
    publishing_house = request.json['publishing_house']
    price = request.json['price']
    ean13 = request.json['ean13']
    isbn = request.json['isbn']
    description = request.json['description']

    new_book = Book(title, author, publishing_house, price, ean13, isbn, description)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)


@app.route("/book", methods=["GET"])
def get_user():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result.data)


@app.route("/book/<id>", methods=["GET"])
def user_detail(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)


@app.route("/book/<id>", methods=["PUT"])
def user_update(id):
    book = Book.query.get(id)
    title = request.json['title']
    author = request.json['author']
    publishing_house = request.json['publishing_house']
    price = request.json['price']
    ean13 = request.json['ean13']
    isbn = request.json['isbn']
    description = request.json['description']

    book.title = title
    book.author = author
    book.publishing_house = publishing_house
    book.price = price
    book.ean13 = ean13
    book.isbn = isbn
    book.description = description

    db.session.commit()
    return book_schema.jsonify(book)


@app.route("/book/<id>", methods=["DELETE"])
def user_delete(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)


if __name__ == '__main__':
    app.run(debug=True)
