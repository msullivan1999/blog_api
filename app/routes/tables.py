from flask import Blueprint, jsonify
from sqlalchemy import text
from app.models import db

tables_bp = Blueprint('tables', __name__)

@tables_bp.route('/create', methods=['GET'])
def create_tables():
    """
    Create all tables based on the models defined in the application.
    Accessible via GET request.
    """
    db.create_all()
    return "Tables created successfully!", 201

@tables_bp.route('/', methods=['GET'])
def list_tables():
    """
    List all tables in the database.
    Accessible via GET request.
    """
    try:
        result = db.session.execute(text("SHOW TABLES")).fetchall()
        tables = [row[0] for row in result]
        return jsonify({"tables": tables}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@tables_bp.route('/databases', methods=['GET'])
def list_databases():
    """
    List all databases in the MySQL instance.
    Accessible via GET request.
    """
    try:
        result = db.session.execute(text('SHOW DATABASES')).fetchall()
        databases = [row[0] for row in result]
        return jsonify({"databases": databases}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400