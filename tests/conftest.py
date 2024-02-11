# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: conftest.py
# ==================================================

# Import modules
import pytest
from application import app as flask_app
from application import db

# App fixture
@pytest.fixture(scope='class')
def app():
    yield flask_app

# Client fixture
@pytest.fixture(scope='class')
def client(app):
    app.config['TESTING'] = True
    print(f"{app.static_url_path} path")

    # Set up a clean test database (helps to ensure any testing done that affects database is NOT stored as temporary clean test database is created every initialization of client)
    with app.app_context():
        db.create_all()
    
    with app.test_client() as client:
        yield client

    # Teardown test database
    with app.app_context():
        db.session.remove()
        db.drop_all()

