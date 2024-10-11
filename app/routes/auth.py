from flask import redirect, url_for, session
from flask_restx import Namespace, Resource
from flask_dance.contrib.google import make_google_blueprint, google
from app.models import db, User
from sqlalchemy.exc import IntegrityError

# Set up the Namespace for authentication
api = Namespace('auth', description='Authentication operations using Google OAuth')

# Google OAuth blueprint (should be registered separately in app/__init__.py)
google_bp = make_google_blueprint(
    client_id='your-client-id',
    client_secret='your-client-secret',
    redirect_to='auth.login',
    scope=["profile", "email"]
)

@api.route("/login")
class Login(Resource):
    @api.doc('login')
    def get(self):
        """
        Log in using Google OAuth.
        Redirects to Google login if not authorized.
        """
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
                return {"error": "An error occurred when trying to create a user"}, 400

        session["user_id"] = user.id
        return redirect(url_for("users.get_users"))

@api.route("/logout")
class Logout(Resource):
    @api.doc('logout')
    def get(self):
        """
        Log out the user by clearing the session.
        """
        session.clear()
        return redirect(url_for("auth.login"))