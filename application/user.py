# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: user.py
# ==================================================

# Import modules
from .models import UserEntry

# UserManager class
class UserManager:
    def __init__(self, database, logger, db_err):
        self.database = database
        self.logger = logger
        self.db_err = db_err

    # ========
    # Add user
    # ========
    def add_user(self, new_entry):
        try:
            self.database.session.add(new_entry)
            self.database.session.commit()
            return new_entry.id
        except Exception as e:
            self.logger.error(f"Failed to add user to database. Error: {str(e)}")
            self.database.session.rollback()
            if "UNIQUE" in str(e):
                raise Exception("Email already exists.")

    # ==========
    # Check user
    # ==========
    def check_user(self, email, password):
        user = UserEntry.query.filter_by(email=email).first()
        if user:
            # If the user exists, check if the password is correct
            if user.password == password:
                return True
        return False
