# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: forms.py
# ==================================================

# Import modules
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired

# =========
# VARIABLES
# =========
input_req = "This input is required."

# ==========
# LOGIN FORM
# ==========
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message=input_req)], render_kw={'placeholder': "Enter your username...", 'id': 'username-input'}) # Username: Admin
    password = PasswordField('Password', validators=[DataRequired(message=input_req)], render_kw={'placeholder': "Enter your password...", 'id': 'password-input'}) # Password: 123ABC
    submit = SubmitField('Login', render_kw={'id':'login-form-submit'})