from flask_restx import Namespace, Resource
from sqlalchemy import text
from app.models import db

# Set up the Namespace for tables
api = Namespace('tables', description='Database table operations')

@api.route('/create')
class CreateTables(Resource):
    @api.doc('create_tables')
    def get(self):
        """
        Create all tables based on the models defined in the application.
        """
        try:
            db.create_all()
            return {"message": "Tables created successfully!"}, 201
        except Exception as e:
            return {"error": str(e)}, 400

@api.route('/')
class ListTables(Resource):
    @api.doc('list_tables')
    def get(self):
        """
        List all tables in the database.
        """
        try:
            result = db.session.execute(text("SHOW TABLES")).fetchall()
            tables = [row[0] for row in result]
            return {"tables": tables}, 200
        except Exception as e:
            return {"error": str(e)}, 400

@api.route('/databases')
class ListDatabases(Resource):
    @api.doc('list_databases')
    def get(self):
        """
        List all databases in the MySQL instance.
        """
        try:
            result = db.session.execute(text('SHOW DATABASES')).fetchall()
            databases = [row[0] for row in result]
            return {"databases": databases}, 200
        except Exception as e:
            return {"error": str(e)}, 400