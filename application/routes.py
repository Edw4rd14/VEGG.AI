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
from flask_cors import CORS, cross_origin
from PIL import Image
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
import re
import base64
import requests
import json
import pickle
import logging
import pytz

# ~~~~~~~~~~~~~~~~~~~~~
# Functions & Variables
# ~~~~~~~~~~~~~~~~~~~~~

# =========
# Variables
# =========

# LABELS
with open('labels.pickle','rb') as file:
    labels = pickle.load(file)
    for key,value in labels.items():
        new_value = value.replace('_',' ')
        labels[key] = new_value
# CONV2D 128x128 MODEL
conv2d_url = "https://ca2-dl-models.onrender.com/v1/models/conv2d128:predict"
# 128x128 IMAGE SIZE
img_128 = (128,128)
# CUSTOMVGG 31x31 MODEL
customvgg_url = "https://ca2-dl-models.onrender.com/v1/models/customvgg31:predict"
# 31x31 IMAGE SIZE
img_31 = (31,31)
# DB ERROR
db_err = "DATABASE ERROR OCCURRED"

# ======
# Logger
# ======
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('err.log')
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
    imgstr = re.search(b'base64,(.*)', img_data).group(1)
    with open('output.png','wb') as output:
        output.write(base64.decodebytes(imgstr))
    im = Image.open('output.png').convert('RGB')
    im.save('output.png')

# ================
# Preprocess Image
# ================
def resize_and_preprocess_image(image_path, target_size):
    # Load the image, grayscale and resize it
    img = image.load_img(image_path, target_size=target_size, color_mode='grayscale')
    # Convert to numpy array and normalize
    img_array = image.img_to_array(img) / 255.0
    # Reshape for model input
    img_array = img_array.reshape((1,) + img_array.shape)
    return img_array

# ===============
# Make Prediction
# ===============
def make_prediction(instances, target_size):
    data = json.dumps({"signature_name": "serving_default", "instances":instances.tolist()})
    headers = {"content-type": "application/json"}
    if target_size[0] == 31:
        url = customvgg_url
    else:
        url = conv2d_url
    json_response = requests.post(url, data=data, headers=headers)
    try:
        predictions = json.loads(json_response.text)['predictions']
    except:
        pass
    return predictions

# ~~~~~~~~~~~~~~~~~~~
# Website page routes
# ~~~~~~~~~~~~~~~~~~~

# ==========
# Login page
# ==========

# Redirect start to login
@app.route('/')
def root():
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    # Clear login failed flag
    session.pop('login_failed', None)
    # Check if form was submitted
    if request.method == 'POST':
        # Flag for login failed first
        session['login_failed'] = True
        # Validate input
        if login_form.validate_on_submit():
            # If username and password are correct
            if login_form.username.data == 'Admin' and login_form.password.data == '123ABC':
                # Clear flag and redirect to index page
                session.pop('login_failed', None)
                return redirect(url_for('index'))
            else:
                # If incorrect, flash error message
                flash(message='Incorrect Credentials.', category='danger')
    return render_template('login.html', form=login_form, show_cards=False, show_button=False, hide_navbar=True)

# =========
# Main page
# =========

# Index page with classifier
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', history=history_manager.get_history())

# ============
# Predict page
# ============

# Prediction page
@app.route('/predict', methods=['GET','POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def predict():
    if request.method == 'POST':
        try:
            # Image data
            data = request.json['image'].encode('utf-8')
            # Image size
            size = int(request.json['image_size'])
            image_size = (size,size)
            # Parse and store image
            parse_image(data)
            # Preprocess image
            img_array = resize_and_preprocess_image("output.png", target_size=image_size)
            # Make prediction based on image size
            predictions = make_prediction(img_array, target_size=image_size)
            # Get label of prediction
            response = labels[np.argmax(predictions)]
            # Add history entry
            new_prediction = Entry(
                file_name = request.json['file_name'],
                image = data,
                image_size= size,
                prediction = response
            )
            # Add entry
            history_manager.add_prediction(new_prediction)
            # Return response
            return response
        except Exception as e:
            return jsonify({"error_message":"An error has occurred! Please try again."}), 500
    else:
        return render_template('index.html', history=history_manager.get_history())



# ==========
# About page
# ==========

# About page
@app.route('/about')
@app.route('/more')
def about():
    return render_template('about.html', show_button=False)