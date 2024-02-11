# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: __init__.py
# ==================================================

# Import modules
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Instantiate database
db = SQLAlchemy()

# Create flask app
app = Flask(__name__)
CORS(app=app)

# Load configuration from config.cfg
app.config.from_pyfile(filename="config.cfg", silent=False)

# Initialize database
with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()
    print("\nDatabase is running...\n")

# Import routes
from application import routes
