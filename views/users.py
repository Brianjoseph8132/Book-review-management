from flask import jsonify, request, Blueprint
from model import db, User, Review
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    
    
    username = data['username']
    email = data['email']
    password = generate_password_hash(data.get('password'))

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    if check_email or check_username:
        return jsonify({"error":"username/email exists"}), 200
    
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Success":"Added successfully"}), 201


# update
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()

    # Ensure the logged-in user is updating their own account
    if user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    username = data.get('username', user.username)
    email = data.get('email', user.email)
    
    # Only hash the password if it is being updated
    password = data.get('password')
    if password:
        password = generate_password_hash(password)
    else:
        password = user.password  # Keep the existing password

    # Check for conflicts with username and email
    check_username = User.query.filter(User.username == username, User.id != current_user_id).first()
    check_email = User.query.filter(User.email == email, User.id != current_user_id).first()

    if check_username or check_email:
        return jsonify({"error": "Username or email already exists"}), 406

    # Update user details
    user.username = username
    user.email = email
    user.password = password

    db.session.commit()
    return jsonify({"success": "Updated successfully"}), 200




# delete
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_users(user_id):
    current_user_id = get_jwt_identity()

    # Ensure the logged-in user is deleting their own account
    if user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User you are trying to delete doesn't exist"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": "Deleted successfully"}), 200




@user_bp.route('/user/books_and_reviews', methods=["GET"])
@jwt_required()  # Ensure the user is authenticated
def books_and_reviews():
    user_id = get_jwt_identity()  # Get the user_id from the JWT token

    reviews = Review.query.filter_by(user_id=user_id).all()

    if not reviews:
        return jsonify({"message": "No books or reviews found for the user."}), 404
    
    response = []
    for review in reviews:
        book = review.book  # Access the associated book using the relationship
        response.append({
            "book_id": book.id,
            "book_title": book.title,
            "book_author": book.author,
            "review_id": review.id,
            "review_text": review.review_text,
            "rating": review.rating,
            "created_at": review.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(response), 200
