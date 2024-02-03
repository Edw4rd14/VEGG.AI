# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: gunicorn_config.py
# ==================================================

bind = "0.0.0.0:8000"
workers = 4
threads = 4
timeout = 120
