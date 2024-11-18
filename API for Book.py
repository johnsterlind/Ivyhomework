from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return "Welcome to the Book API!"

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    # Validate required fields
    if not all(k in data for k in ("id", "book_name", "author", "publisher")):
        return jsonify({"error": "Missing required fields"}), 400
    # Check for duplicate IDs
    if Book.query.get(data["id"]):
        return jsonify({"error": "Book with this ID already exists"}), 400
    # Add the new book to the database
    new_book = Book(
        id=data["id"],
        book_name=data["book_name"],
        author=data["author"],
        publisher=data["publisher"]
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully"}), 201

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([
        {"id": book.id, "book_name": book.book_name, "author": book.author, "publisher": book.publisher}
        for book in books
    ])

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if "book_name" in data:
        book.book_name = data["book_name"]
    if "author" in data:
        book.author = data["author"]
    if "publisher" in data:
        book.publisher = data["publisher"]
    db.session.commit()
    return jsonify({"message": "Book updated successfully"}), 200

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)