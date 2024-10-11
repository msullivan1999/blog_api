from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import text
import argparse

app = Flask(__name__)

# Replace with your actual MySQL configuration details

parser = argparse.ArgumentParser(description="Run Flask with MySQL credentials")
parser.add_argument('--db_user', required=True, help='MySQL database user')
parser.add_argument('--db_password', required=True, help='MySQL database password')
parser.add_argument('--db_host', required=True, help='MySQL database host')
parser.add_argument('--db_name', required=True, help='MySQL database name')

args = parser.parse_args()

# Configuring SQLAlchemy with MySQL connection using PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{args.db_user}:{args.db_password}@{args.db_host}/{args.db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy event system

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define a 'User' model to create the 'users' table
class User(db.Model):
    __tablename__ = 'users'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.name}>'

# Route to create all tables (Run once to create the 'users' table)
@app.route('/create_tables')
def create_tables():
    db.create_all()
    return "Tables created!"

# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        # Get the 'name' and 'email' from the request
        name = request.json['name']
        email = request.json['email']

        # Create a new User instance
        new_user = User(name=name, email=email)

        # Add the new user to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": f"User {name} added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Query all users
        users = User.query.all()

        # Return a list of users
        users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]

        return jsonify(users_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/tables', methods=['GET'])
def list_tables():
    try:
        # Execute a query to get the list of tables
        result = db.session.execute(text("SHOW TABLES")).fetchall()
        tables = [row[0] for row in result]  # Extract table names from the result

        return jsonify({"tables": tables}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to check connection and databases
@app.route('/')
def index():
    try:
        # Checking connection by querying system information
        result = db.session.execute(text('SHOW DATABASES')).fetchall()
        return f"Connected to MySQL! Databases: {result}"

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080)