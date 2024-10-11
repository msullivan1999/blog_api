from flask import redirect, url_for, session, jsonify
from flask_restx import Namespace, Resource
from flask_dance.contrib.google import google
from app.models import db, User
from sqlalchemy.exc import IntegrityError

# Set up the Namespace for authentication
api = Namespace('auth', description='Authentication operations using Google OAuth')

@api.route("/login")
class Login(Resource):
    @api.doc('login')
    def get(self):
        """
        Log in using Google OAuth.
        Redirects to Google login if not authorized.
        """
        if not google.authorized:
            # Make sure this route name matches how the Google blueprint is registered
            return redirect(url_for("google.login"))

        # Fetch user info from Google
        resp = google.get("/oauth2/v1/userinfo")
        print("yay got here!")
        if not resp or not resp.ok:
            return {"error": "Failed to fetch user info from Google"}, 400

        user_info = resp.json()
        email = user_info.get("email")
        google_id = user_info.get("id")

        # Ensure email and google_id are present in the response
        if not email or not google_id:
            return {"error": "Incomplete user information from Google"}, 400

        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            # Create a new user if one does not exist
            try:
                user = User(name=user_info.get("name"), email=email, google_id=google_id)
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return {"error": "An error occurred when trying to create a user"}, 400

        session["user_id"] = user.id
        return redirect(url_for("users.get_users"))  # Make sure this matches your users route setup

@api.route("/logout")
class Logout(Resource):
    @api.doc('logout')
    def get(self):
        """
        Log out the user by clearing the session.
        """
        session.clear()
        return redirect(url_for("auth.login"))