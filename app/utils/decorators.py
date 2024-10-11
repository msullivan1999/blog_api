from functools import wraps
from flask import request, redirect, url_for, session, jsonify
from app.models import User

def require_auth(func):
    """
    Decorator to ensure the user is authenticated.
    If the user is not logged in, it redirects to the login page.
    """
    @wraps(func)  # This preserves the original function's name and metadata
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Invalid session or user not found"}), 401

        # Pass the user object to the route handler if needed
        return func(*args, **kwargs)
    
    return decorated_function

def admin_required(func):
    """
    Decorator to ensure the user is an admin.
    If the user is not an admin, it returns a 403 Forbidden response.
    """
    @wraps(func)  # This preserves the original function's name and metadata
    @require_auth
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        user = User.query.get(user_id)

        if not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403

        # Pass the user object to the route handler if needed
        return func(*args, **kwargs)

    return decorated_function