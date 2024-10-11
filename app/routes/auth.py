from flask import Blueprint, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
from app.models import db, User
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

# Google OAuth blueprint
google_bp = make_google_blueprint(
    client_id='your-client-id',
    client_secret='your-client-secret',
    redirect_to='auth.login',
    scope=["profile", "email"]
)

@auth_bp.route("/login")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v1/userinfo")
    user_info = resp.json()
    email = user_info["email"]
    google_id = user_info["id"]

    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        # Create a new user if one does not exist
        try:
            user = User(name=user_info["name"], email=email, google_id=google_id)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "An error occurred when trying to create a user", 400

    session["user_id"] = user.id
    return redirect(url_for("users.get_users"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))