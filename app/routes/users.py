from flask import Blueprint, request, jsonify
from app.models import db, User

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
def add_user():
    """
    Add a new user.
    Accessible to everyone (no authentication required).
    """
    try:
        name = request.json.get('name')
        email = request.json.get('email')

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": f"User {name} added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/', methods=['GET'])
def get_users():
    """
    Get all users.
    Accessible to everyone (no authentication required).
    """
    try:
        users = User.query.all()
        users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a single user based on the user ID.
    Accessible to everyone (no authentication required).
    """
    try:
        user = User.query.get_or_404(user_id)
        user_data = {"id": user.id, "name": user.name, "email": user.email}
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400