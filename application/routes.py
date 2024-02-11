# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: routes.py
# ==================================================

# Import modules
from application import app, db
from application.models import Entry
from application.history import PredictionHistoryManager
from application.forms import LoginForm
from flask import render_template, request, flash, redirect, url_for, jsonify, session
from flask_cors import cross_origin
from PIL import Image
from tensorflow.keras.preprocessing import image
import numpy as np
import re
import base64
import requests
import json
import pickle
import logging

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
    json_response = requests.post(url, data=data, headers=headers) # nosec
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
    login_form = LoginForm()
    # Clear login failed flag
    session.pop("login_failed", None)
    # Check if form was submitted
    if request.method == "POST":
        # Flag for login failed first
        session["login_failed"] = True
        # Validate input
        if login_form.validate_on_submit():
            # If username and password are correct
            if (
                login_form.username.data == "Admin"
                and login_form.password.data == "123ABC"
            ):
                # Clear flag and redirect to index page
                session.pop("login_failed", None)
                return redirect(url_for("index"))
            else:
                # If incorrect, flash error message
                flash(message="Incorrect Credentials.", category="danger")
    return render_template(
        "login.html",
        form=login_form,
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
@app.route("/api/get", methods=["GET"])
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
