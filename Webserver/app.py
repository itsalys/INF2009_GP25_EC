from flask import Flask
from Database.db_connection import db, DATABASE_URI
from Database.db_setup import init_db
from Routes import register_routes

app = Flask(__name__)

# Configure Database URI
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db.init_app(app)

# Ensure database exists and create tables if needed
init_db(app)

# Register routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
