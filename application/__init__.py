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

# Create flask app
app = Flask(__name__)
CORS(app=app)

# Load configuration from config.cfg
app.config.from_pyfile(filename='config.cfg', silent=False)

# Import routes
from application import routes


