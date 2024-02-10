# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: models.py
# ==================================================

# Import modules
from application import db
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint
from sqlalchemy import Column, String, BLOB

# Database entry class
class Entry(db.Model):
    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column('file_name',db.String(100), nullable=False)
    image = db.Column('image',db.BLOB, nullable=False)
    image_size = db.Column('image_size',db.Integer, nullable=False)
    prediction = db.Column('prediction',db.String(30),nullable=False)
    timestamp = db.Column('timestamp',db.DateTime, nullable=False, default=func.now()) # Get current timestamp
    # Check constraints
    __table_args__ = (
        CheckConstraint('image_size = 31 OR image_size = 128'),
        CheckConstraint("prediction IN ('Bean', 'Bitter Gourd', 'Bottle Gourd', 'Brinjal', 'Broccoli', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber', 'Papaya', 'Potato', 'Pumpkin', 'Radish', 'Tomato')"),
    )
    # Table name
    __tablename__ = 'prediction_entries'