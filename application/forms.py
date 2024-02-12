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
from wtforms.validators import DataRequired, Email, Regexp

# =========
# VARIABLES
# =========
input_req = "This input is required."
password_req = "Password must contain at least 1 uppercase letter, 1 lowercase letter, and be at least 8 characters long."

# ==========
# LOGIN FORM
# ==========
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message=input_req),
            Email(message="Invalid email address."),
        ],
        render_kw={"placeholder": "Enter your email...", "id": "email-input"},
    )  # Username: Admin
    password = PasswordField(
        "Password",
        validators=[DataRequired(message=input_req)],
        render_kw={"placeholder": "Enter your password...", "id": "password-input"},
    )  # Password: 123ABC
    submit = SubmitField("Login", render_kw={"id": "login-form-submit"})


# ============
# SIGN UP FORM
# ============
class SignUpForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message=input_req),
            Email(message="Invalid email address."),
        ],
        render_kw={"placeholder": "Enter your email...", "id": "signup-email-input"},
    )
    username = StringField(
        "Username",
        validators=[DataRequired(message=input_req)],
        render_kw={
            "placeholder": "Enter your username...",
            "id": "signup-username-input",
        },
    )  # Username: Admin
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message=input_req),
            Regexp(regex=r"^(?=.*[a-z])(?=.*[A-Z]).{8,}$", message=password_req),
        ],
        render_kw={
            "placeholder": "Enter your password...",
            "id": "signup-password-input",
        },
    )  # Password: 123ABC
    submit = SubmitField("Sign up", render_kw={"id": "signup-form-submit"})
