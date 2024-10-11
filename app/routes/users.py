from flask import request, session
from flask_restx import Namespace, Resource, fields
from app.models import db, User
from app.utils.decorators import require_auth

# Set up the Namespace for users
api = Namespace('users', description='User-related operations')

# Define a model for the user using Flask-RESTx
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user identifier'),
    'name': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
    'google_id': fields.String(readonly=True, description='The Google OAuth ID of the user'),
    'is_admin': fields.Boolean(readonly=True, description='Admin flag to indicate if the user is an admin'),
    'created_at': fields.DateTime(readonly=True, description='The timestamp when the user was created')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """
        List all users.
        Accessible to everyone (no authentication required).
        """
        try:
            users = User.query.all()
            return users, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        """
        Create a new user.
        Accessible to everyone (no authentication required).
        """
        try:
            data = request.json
            name = data.get('name')
            email = data.get('email')
            google_id = data.get('google_id')
            is_admin = data.get('is_admin', False)  # Default to False if not provided

            if not name or not email or not google_id:
                return {"error": "Name, email, and google_id are required"}, 400

            new_user = User(name=name, email=email, google_id=google_id, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"User {name} added successfully!"}, 201
        except Exception as e:
            return {"error": str(e)}, 400

@api.route('/<int:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """
        Get a single user based on the user ID.
        Accessible to everyone (no authentication required).
        """
        try:
            user = User.query.get_or_404(user_id)
            return user, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.doc('update_user')
    @api.expect(user_model)
    @require_auth
    def put(self, user_id):
        """
        Update user details.
        Accessible only to authenticated users.
        """
        try:
            user = User.query.get_or_404(user_id)
            data = request.json
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.is_admin = data.get('is_admin', user.is_admin)  # Only allow changing if explicitly provided
            db.session.commit()
            return {"message": f"User {user.name} updated successfully!"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.doc('delete_user')
    @require_auth
    def delete(self, user_id):
        """
        Delete a user.
        Accessible only to authenticated users.
        """
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": f"User {user.name} deleted successfully!"}, 200
        except Exception as e:
            return {"error": str(e)}, 400