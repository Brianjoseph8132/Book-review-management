from flask import jsonify, request, Blueprint
from model import db, Book
from datetime import datetime

book_bp = Blueprint("book_bp", __name__)

# ==================books==============
@book_bp.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    title = data['title']
    author = data['author']
    genre = data['genre']
    published_date = data['published_date']


    check_title = Book.query.filter_by(title=title).first()

    if check_title:
        return jsonify({"error": "Title already exists"}), 406
    
    # Validate and parse published date
    try:
        published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid published_date format. Use 'YYYY-MM-DD'"}), 400
    

    # Create and add the new book
    new_book = Book(
        title=title,
        author=author,
        genre=genre,
        published_date=published_date,
        
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"success": "Book added successfully"}), 201


# update
@book_bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id)

    if book:
        # Extract data from the request
        title = data.get('title', book.title)
        author = data.get('author', book.author)
        genre = data.get('genre', book.genre)
        published_date = data.get('published_date', book.published_date)


        check_book_id =Book.query.get(book_id)

        if not check_book_id:
            return jsonify({"error":"Book not found"}), 404
        
        # apply the updates
        book.title=title
        book.author=author
        book.genre=genre
        book.published_date=published_date

        # Convert published_date to a date object if necessary
        if published_date:
            try:
                book.published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid published_date format. Use 'YYYY-MM-DD'"}), 400

        db.session.commit()
        return jsonify({"success": "Book updated successfully"}), 200
    
    else:
        return jsonify({"error": "Book not found"}), 404
    



# fetch
@book_bp.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()

    book_list = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "published_date": book.published_date.strftime("%Y-%m-%d") if isinstance(book.published_date, datetime) else str(book.published_date) if book.published_date else None,
            "reviews": [
                {
                    "review_id": review.id,
                    "review_text": review.review_text,
                    "rating": review.rating,
                    "user_id": review.user_id,
                    "created_at": review.created_at.strftime("%Y-%m-%d %H:%M:%S")
                } for review in book.reviews  # Access the associated reviews
            ]
        } for book in books
    ]

    return jsonify(book_list), 200



# delete
@book_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_books(book_id):
    book = Book.query.get(book_id)

    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"Success":"Deleted successfully"}),200
    

    else:
        return jsonify({"error":"Book you are trying to delete doesn't exist"}),406