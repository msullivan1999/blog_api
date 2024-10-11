from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv
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


    # Register Google OAuth blueprint
    google_bp = make_google_blueprint(
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        redirect_to='auth.login',
        scope=["profile", "email"]
    )
    app.register_blueprint(google_bp, url_prefix="/login")

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.posts import posts_bp
    from app.routes.comments import comments_bp
    from app.routes.likes import likes_bp
    from app.routes.tables import tables_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(posts_bp, url_prefix="/posts")
    app.register_blueprint(comments_bp, url_prefix="/comments")
    app.register_blueprint(likes_bp, url_prefix="/likes")
    app.register_blueprint(tables_bp, url_prefix="/tables")

    return app