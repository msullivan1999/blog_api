from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv
from flask_restx import Api
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Fetch database credentials from environment variables
    db_user = os.environ.get('DB_USER', 'default_user')
    db_password = os.environ.get('DB_PASSWORD', 'default_password')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_name = os.environ.get('DB_NAME', 'default_db')
    unix_socket_path = os.environ.get("INSTANCE_UNIX_SOCKET")

    # Configure the database connection
    if unix_socket_path:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@/{db_name}?unix_socket={unix_socket_path}'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')  # Required for session management

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Set up Flask-RESTx API
    api = Api(app, version='1.0', title='Blog API',
    description='A simple Flask Blog API with Swagger documentation',
    doc='/docs')  # Swagger UI available at /docs

 # Set up and register the Google OAuth blueprint
    google_bp = make_google_blueprint(
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        redirect_to='google.authorized',  # Redirect to the function handling post-auth
        scope=["profile", "email"],
    )
    app.register_blueprint(google_bp, url_prefix="/auth")


    # Register namespaces
    from app.routes.auth import api as auth_ns
    from app.routes.users import api as users_ns
    from app.routes.posts import api as posts_ns
    from app.routes.comments import api as comments_ns
    from app.routes.likes import api as likes_ns
    from app.routes.tables import api as tables_ns

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(posts_ns, path='/posts')
    api.add_namespace(comments_ns, path='/comments')
    api.add_namespace(likes_ns, path='/likes')
    api.add_namespace(tables_ns, path='/tables')

    return app