from flask import jsonify, request,Blueprint
from model import db, User, Review, Book
from flask_jwt_extended import jwt_required, get_jwt_identity

review_bp = Blueprint("review_bp", __name__)


# ================reviews===========
@review_bp.route("/reviews", methods=["POST"])
@jwt_required()
def add_review():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    # Extract and validate inputs
    review_text = data.get('review_text')
    rating = data.get('rating')
    book_id = data.get('book_id')

    if not review_text or not rating or not book_id:
        return jsonify({"error": "review_text, rating, and book_id are required"}), 400

    # Validate the book_id
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Invalid book_id. The book does not exist."}), 404

    # Check if the user has already reviewed this book
    check_review = Review.query.filter_by(book_id=book_id, user_id=current_user_id).first()
    if check_review:
        return jsonify({
            "error": f"You have already reviewed the book '{book.title}'",
            "existing_review": {
                "review_text": check_review.review_text,
                "rating": check_review.rating
            }
        }), 406

    # Create and add the new review
    new_review = Review(
        review_text=review_text,
        rating=rating,
        book_id=book_id,
        user_id=current_user_id,
    )
    db.session.add(new_review)
    db.session.commit()

    return jsonify({"success": "Review added successfully"}), 201


@review_bp.route("/reviews/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review(review_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    review = Review.query.get(review_id)

    if not review:
        return jsonify({"error": "Review not found"}), 404

    # Ensure the review belongs to the current user
    if review.user_id != current_user_id:
        return jsonify({"error": "You are not authorized to update this review"}), 403

    # Extract data from the request safely
    review_text = data.get('review_text', review.review_text)
    rating = data.get('rating', review.rating)
    book_id = data.get('book_id', review.book_id)

    # Check for conflicting reviews for the same book by the same user
    check_review = Review.query.filter(
        Review.book_id == book_id,
        Review.user_id == review.user_id,
        Review.id != review_id
    ).first()

    if check_review:
        return jsonify({"error": "A conflicting review exists"}), 409

    # Apply the updates
    review.review_text = review_text
    review.rating = rating
    review.book_id = book_id

    db.session.commit()
    return jsonify({"success": "Review updated successfully"}), 200


# fetch
@review_bp.route("/reviews", methods=["GET"])
@jwt_required()
def get_reviews():
    # Get the current user's ID
    current_user_id = get_jwt_identity()

    # Fetch reviews for the current user
    reviews = Review.query.filter_by(user_id=current_user_id).all()

    if not reviews:
        return jsonify({"message": "No reviews found for the current user."}), 404

    # Create a list of reviews with book details
    review_list = [
        {
            "id": review.id,
            "review_text": review.review_text,
            "rating": review.rating,
            "book_id": review.book_id,
            "user_id": review.user_id,
            "book": {
                "id": review.book.id,
                "title": review.book.title,
                "author": review.book.author,
                "genre": review.book.genre,
                "published_date": review.book.published_date
            } if review.book else None,
        }
        for review in reviews
    ]

    return jsonify(review_list), 200



@review_bp.route("/reviews/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_reviews(review_id):
    current_user_id = get_jwt_identity()
    
    # Fetch the review by ID and ensure it belongs to the current user
    review = Review.query.filter_by(id=review_id, user_id=current_user_id).first()

    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"Success": "Deleted successfully"}), 200
    else:
        return jsonify({"error": "Review you are trying to delete doesn't exist or doesn't belong to you"}), 404
