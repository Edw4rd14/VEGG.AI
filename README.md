# 🥬 VEGG.AI

<b>NAME</b>: EDWARD TAN YUAN CHONG

<b>CLASS</b>: DAAA/FT/2B/04

<b>ADM NO.</b>: 2214407

<b>Description:</b>

The website is titled "Vegg.AI", which is a web application that allows users to upload an image of a vegetable, select their desired image input size of 31x31 pixels or 128x128 pixels, and receive a prediction from our AI model trained to classify vegetables, with an outstanding accuracy of 99%. This website was created as a part of my DevOps and AI Automation assignment.

<b>Guide on setting up model notebook, model.ipynb (in VEGG.AI-MODELS repository):</b>
- Clone this local repository (VEGG.AI-MODELS) into your machine.
- Obtain the testing image folder if possible for evaluation (otherwise you could skip the evaluations)
- Next, redirect your Git Bash terminal to the folder <i>vegg.ai-models</i>.
- In you Git Bash terminal, run `python -m venv env` to create the virtual environment, followed by `source ./env/bin/activate` to activate the virtual environment.
- To install the dependencies for this notebook, run `pip install -r requirements.txt`.
- With that, you can run the model.ipynb to obtain the most updated models.

<b>Guide on starting the website locally:</b>
- Clone this local repository into your machine.
- Next, redirect your Git Bash terminal to the folder <i>vegg.ai</i>.
- In you Git Bash terminal, run `python -m venv env` to create the virtual environment, followed by `source ./env/bin/activate` to activate the virtual environment.
- To install the dependencies to run the website, run `pip install -r requirements.txt`.
- With that, run `python -m flask run`.

<b>Guide on running pytest:</b>
- Clone this local repository into your machine.
- Next, redirect your Git Bash terminal to the folder <i>vegg.ai</i>.
- In you Git Bash terminal, run `python -m venv env` to create the virtual environment, followed by `source ./env/bin/activate` to activate the virtual environment.
- To install the dependencies to run the website, run `pip install -r requirements.txt`.
- With that, to run the RESTful API tests, run `python -m pytest tests/test_api.py -p no:randomly -v`.
- To run the application tests, run `python -m pytest tests/test_application.py --randomly-seed=14 -v`

<b>Model links on Render.com:</b>
- Conv2D for 128x128 images: https://ca2-dl-models.onrender.com/v1/models/conv2d128
- CustomVGG for 31x31 images: https://ca2-dl-models.onrender.com/v1/models/customvgg31 

<b>Final website link for Vegg.AI:</b> https://vegg-ai.onrender.com

🤓 Thank you for visiting!
