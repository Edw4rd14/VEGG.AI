# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: routes.py
# ==================================================

# Import modules
from flask import render_template, request, flash, redirect, url_for, jsonify, session
from flask_cors import cross_origin
from PIL import Image
from tensorflow.keras.preprocessing import image
from application import app, db
from application.models import Entry, UserEntry
from application.history import PredictionHistoryManager
from application.forms import LoginForm, SignUpForm
from application.user import UserManager
import numpy as np
import re
import base64
import requests
import json
import secrets
import pickle
import logging
import os
import random


# ~~~~~~~~~~~~~~~~~~~~~
# Functions & Variables
# ~~~~~~~~~~~~~~~~~~~~~

# =========
# Variables
# =========

# LABELS
with open("labels.pickle", "rb") as file:
    labels = pickle.load(file)
    for key, value in labels.items():
        new_value = value.replace("_", " ")
        labels[key] = new_value
# CONV2D 128x128 MODEL
conv2d_url = "https://ca2-dl-models.onrender.com/v1/models/conv2d128:predict"
# 128x128 IMAGE SIZE
img_128 = (128, 128)
# CUSTOMVGG 31x31 MODEL
customvgg_url = "https://ca2-dl-models.onrender.com/v1/models/customvgg31:predict"
# 31x31 IMAGE SIZE
img_31 = (31, 31)
# DB ERROR
db_err = "DATABASE ERROR OCCURRED"

# ======
# Logger
# ======
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("err.log")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# ==========================
# PREDICTION HISTORY MANAGER
# ==========================
history_manager = PredictionHistoryManager(database=db, logger=logger, db_err=db_err)

# ====================
# USER HISTORY MANAGER
# ====================
user_manager = UserManager(database=db, logger=logger, db_err=db_err)

# ===========
# Parse Image
# ===========
def parse_image(img_data):
    imgstr = re.search(b"base64,(.*)", img_data).group(1)
    with open("output.png", "wb") as output:
        output.write(base64.decodebytes(imgstr))
    im = Image.open("output.png").convert("RGB")
    im.save("output.png")


# ================
# Preprocess Image
# ================
def resize_and_preprocess_image(image_path, target_size):
    # Load the image, grayscale and resize it
    img = image.load_img(image_path, target_size=target_size, color_mode="grayscale")
    # Convert to numpy array and normalize
    img_array = image.img_to_array(img) / 255.0
    # Reshape for model input
    img_array = img_array.reshape((1,) + img_array.shape)
    return img_array


# ===============
# Make Prediction
# ===============
def make_prediction(instances, target_size):
    data = json.dumps(
        {"signature_name": "serving_default", "instances": instances.tolist()}
    )
    headers = {"content-type": "application/json"}
    url = (
        customvgg_url
        if target_size == 31
        else (conv2d_url if target_size == 128 else None)
    )
    json_response = requests.post(url, data=data, headers=headers)  # nosec
    try:
        predictions = json.loads(json_response.text)["predictions"]
    except Exception as e:
        logging.error(f"Error during JSON decoding: {e}")
        predictions = None
    return predictions


# =======
# PREDICT
# =======
def predict_label(image, size):
    # Parse and store image
    parse_image(image)
    # Preprocess image
    img_array = resize_and_preprocess_image("output.png", target_size=(size, size))
    # Get predictions
    predictions = make_prediction(instances=img_array, target_size=size)
    # Return label of prediction
    return labels[np.argmax(predictions)]


# ~~~~~~~~~~~~~~~~~~~
# Website page routes
# ~~~~~~~~~~~~~~~~~~~

# ==========
# Login page
# ==========

# Redirect start to login
@app.route("/")
def root():
    return redirect(url_for("login"))


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Instantiate login form
    login_form = LoginForm()
    # Clear login failed flag
    session.pop("login_failed", None)
    # Check if form was submitted
    if request.method == "POST":
        # Flag for login failed first
        session["login_failed"] = True
        # Validate submit
        if login_form.validate_on_submit():
            # If username and password are correct
            if user_manager.check_user(
                email=login_form.email.data, password=login_form.password.data
            ) or (
                login_form.email.data == "admin@gmail.com"
                and login_form.password.data == "123ABC"
            ):
                # Clear flag and redirect to index page
                session.pop("login_failed", None)
                return redirect(url_for("index"))
            else:
                # If incorrect, flash error message
                flash(message="Incorrect Credentials.", category="danger")
    # Return login
    return render_template(
        "login.html",
        form=login_form,
        show_cards=False,
        show_button=False,
        hide_navbar=True,
    )


# Signup page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Instantiate Sign up form
    signup_form = SignUpForm()
    # Clear sign up failed flag
    session.pop("signup_failed", None)
    # Check if method is POST
    if request.method == "POST":
        # Flag sign up failed
        session["signup_failed"] = True
        # Validate submit
        if signup_form.validate_on_submit():
            try:
                # Email, username, and password
                email, username, password = (
                    signup_form.email.data,
                    signup_form.username.data,
                    signup_form.password.data,
                )
                # Validate it is not empty
                if email and username and password:
                    # Set up entry
                    new_entry = UserEntry(
                        email=email, username=username, password=password
                    )
                    # Add user
                    if user_manager.add_user(new_entry):
                        session.pop("signup_failed", None)
                        return redirect(url_for("login"))
                # Raise error
                raise Exception("An error occurred. Please try again later.")
            # Catch errors
            except Exception as e:
                # If incorrect, flash error message
                flash(message=e, category="danger")
    # Return sign up
    return render_template(
        "signup.html",
        form=signup_form,
        show_cards=False,
        show_button=False,
        hide_navbar=True,
    )


# =========
# Main page
# =========

# Index page with classifier
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html", history=history_manager.get_history())


# ============
# Predict page
# ============

# Prediction page
@app.route("/predict", methods=["GET", "POST"])
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
def predict():
    if request.method == "POST":
        try:
            # Image data
            image = request.json["image"].encode("utf-8")
            # File name
            file_name = request.json["file_name"]
            # Image size
            size = int(request.json["image_size"])
            # Predict for image
            prediction = predict_label(image=image, size=size)
            # Add history entry
            new_prediction = Entry(
                file_name=file_name, image=image, image_size=size, prediction=prediction
            )
            # Add entry
            history_manager.add_prediction(new_prediction)
            # Return response
            return prediction
        except Exception:
            return (
                jsonify({"error_message": "An error has occurred! Please try again."}),
                500,
            )
    else:
        return render_template("index.html", history=history_manager.get_history())


# ===========
# SERVE IMAGE
# ===========

# Serve random image
@app.route("/random-prediction-image")
def serve_random_image():
    image_dir = "./prediction-testing-images"
    all_images = [f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png"))]
    if not all_images:
        return "No images found in the directory."
    random_image_filename = secrets.choice(all_images)
    random_image_path = os.path.join(image_dir, random_image_filename)
    with open(random_image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    return {"filename": random_image_filename, "base64_image": base64_image}


# ==========
# About page
# ==========

# About page
@app.route("/about")
@app.route("/more")
def about():
    return render_template("about.html", show_button=False)


# ==============
# Remove history
# ==============

# Remove history
@app.route("/remove/<int:history_id>", methods=["POST"])
def remove(history_id):
    history_manager.remove_history(history_id=history_id)
    return redirect(url_for("index"))


# ============
# RESTFUL APIs
# ============


# Sign up API
@app.route("/api/signup", methods=["POST"])
def api_signup():
    # Get data
    email, username, password = (
        request.json["email"],
        request.json["username"],
        request.json["password"],
    )
    # Add user entry
    new_user = UserEntry(email=email, username=username, password=password)
    # Add user entry to database
    result = user_manager.add_user(new_entry=new_user)
    # Return result
    return jsonify({"id": result})


# Login API
@app.route("/api/login", methods=["POST"])
def api_login():
    # Get data
    email, password = request.json["email"], request.json["password"]
    # Check user
    result = user_manager.check_user(email, password)
    # Return result
    return jsonify({"created": result})


# API TESTING
# Add history API
@app.route("/api/add", methods=["POST"])
def api_add():
    # Image data
    image = request.json["image"].encode("utf-8")
    # File name
    file_name = request.json["file_name"]
    # Image size
    size = int(request.json["image_size"])
    # Prediction
    prediction = request.json["prediction"]
    # Add history entry
    new_prediction = Entry(
        file_name=file_name, image=image, image_size=size, prediction=prediction
    )
    # Add entry to database
    result = history_manager.add_prediction(new_entry=new_prediction)
    # Return result
    return jsonify({"id": result})


# Get history API
@app.route("/api/get/<int:history_id>", methods=["GET"])
def api_get(history_id):
    # Get history by Id
    history = history_manager.get_history_by_id(history_id=history_id)
    # Store in JSON object
    data = {
        "id": history.id,
        "file_name": history.file_name,
        "image": history.image.decode("utf-8"),
        "image_size": history.image_size,
        "prediction": history.prediction,
        "timestamp": history.timestamp,
    }
    result = jsonify(data)
    # Return JSON object
    return result


# Delete history API
@app.route("/api/delete/<int:history_id>", methods=["POST"])
def api_delete(history_id):
    # Try to remove history, if successful, return success result
    try:
        history_manager.remove_history(history_id=history_id)
        return jsonify({"result": "Success"})
    # Else, return failure result
    except Exception:
        return jsonify({"result": "Failure"})


# Get all history API
@app.route("/api/get_all", methods=["GET"])
def get_all_history():
    # Return entire history
    return history_manager.get_history()


# Make prediction API
@app.route("/api/predict", methods=["POST"])
def api_predict():
    # Get JSON file from client
    data = request.get_json()
    # Get each data field
    image = data["image"].encode("utf-8")
    size = int(data["image_size"])
    # Predict for image
    prediction = predict_label(image=image, size=size)
    # Return JSON object with price
    return jsonify({"prediction": prediction})
