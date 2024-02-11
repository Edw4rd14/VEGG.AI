# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: history.py
# ==================================================

# Import modules
import pytz
from application.models import Entry
import base64
import re

# Prediction History Manager class
class PredictionHistoryManager:
    def __init__(self, database, logger, db_err):
        self.database = database
        self.logger = logger
        self.db_err = db_err

    def add_prediction(self, new_entry):
        try:
            self.database.session.add(new_entry)
            self.database.session.commit()
            return new_entry.id
        except Exception as e:
            self.logger.error(f"Failed to add prediction to history. Error: {str(e)}")
            self.database.session.rollback()
    # ===========
    # Get History
    # ===========
    def get_history(self):
        try:
            history = self.database.session.execute(self.database.select(Entry).order_by(Entry.id)).scalars()
            history_list = list(history)
            # Define the Singapore timezone
            sg_tz = pytz.timezone('Asia/Singapore')
            # Convert each timestamp to SGT and decode image
            for entry in history_list:
                entry.timestamp = entry.timestamp.replace(tzinfo=pytz.utc).astimezone(sg_tz)
                entry.image = entry.image.decode('utf-8')
            return history_list
        except Exception as e:
            self.database.session.rollback()
            self.logger.error(f"Failed to get history. Error: {str(e)}")
            return []
    # ==============
    # Remove History
    # ==============
    def remove_history(self, history_id):
        try:
            history = self.database.get_or_404(Entry, history_id)
            self.database.session.delete(history)
            self.database.session.commit()
        except Exception as e:
            self.database.session.rollback()
            self.logger.error(f"Failed to remove history with ID {history_id}. Error: {str(e)}")
            return 0

    # ==================
    # Get Specific Image
    # ==================
    def get_history_by_id(self, history_id):
        try:
            result = self.database.get_or_404(Entry, history_id)
            return result
        except Exception as e:
            self.database.session.rollback()
            self.logger.error(f"Failed to get history with ID {history_id}. Error: {str(e)}")
            return 0