# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: routes.py
# ==================================================

# Import modules
from application import app
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
import numpy as np

# ==========
# Login page
# ==========
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

# =========
# Main page
# =========
@app.route('/index')
@app.route('/home')
@app.route('/')
def main():
    return render_template('index.html')

# ============
# Predict page
# ============
@app.route('/predict', methods=['GET','POST'])
def predict():
    return render_template('index.html')

# ==========
# About page
# ==========
@app.route('/about')
@app.route('/more')
def about():
    return render_template('about.html')
