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

# Main page
@app.route('/index')
@app.route('/home')
@app.route('/')
def main():
    return render_template('index.html')