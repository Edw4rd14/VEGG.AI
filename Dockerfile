# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: Dockerfile
# ==================================================

# Pull python version
FROM python:3.8.18

# Set working directory
WORKDIR /ca2-daaa2b04-2214407-edward-webapp

# copy every content from the local file to the image
COPY . /ca2-daaa2b04-2214407-edward-webapp

# Install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Expose the Flask default port
EXPOSE 5000

# Run the Flask application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]