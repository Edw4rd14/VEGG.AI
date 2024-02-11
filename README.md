# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT

<b>REPOSITORY</b>: CA2-DAAA2B04-2214407-EDWARD-WEBAPP

<b>NAME</b>: EDWARD TAN YUAN CHONG

<b>CLASS</b>: DAAA/FT/2B/04

<b>ADM NO.</b>: 2214407

<b>Description:</b>

This is my GitLab repository for the DevOps and Automation for AI (DOAA) CA2 Project on MLOPS for Deep Learning Web Application.

The website is titled "Vegg.AI", which is a web application that allows users to upload an image of a vegetable, select their desired image input size of 31x31 pixels or 128x128 pixels, and receive a prediction from our AI model trained to classify vegetables, with an outstanding accuracy of 99%. 

<b>Guide on setting up model notebook, model.ipynb (in CA2-DAAA2B04-2214407-EDWARD repository):</b>
- Clone this local repository (CA2-DAAA2B04-2214407-EDWARD) into your machine.
- Obtain the testing image folder if possible for evaluation (otherwise you could skip the evaluations)
- Next, redirect your Git Bash terminal to the folder <i>ca2-daaa2b04-2214407-edward</i>.
- In you Git Bash terminal, run `python -m venv env` to create the virtual environment, followed by `source ./env/bin/activate` to activate the virtual environment.
- To install the dependencies for this notebook, run `pip install -r requirements.txt`.
- With that, you can run the model.ipynb to obtain the most updated models.

<b>Guide on starting the website locally:</b>
- Clone this local repository (CA2-DAAA2B04-2214407-EDWARD-WEBAPP) into your machine.
- Next, redirect your Git Bash terminal to the folder <i>ca2-daaa2b04-2214407-edward-webapp</i>.
- In you Git Bash terminal, run `python -m venv env` to create the virtual environment, followed by `source ./env/bin/activate` to activate the virtual environment.
- To install the dependencies to run the website, run `pip install -r requirements.txt`.
- With that, run `python -m flask run`.

<b>Guide on running pytest:</b>
- Clone this local repository (CA2-DAAA2B04-2214407-EDWARD-WEBAPP) into your machine.
- Next, redirect your Git Bash terminal to the folder <i>ca2-daaa2b04-2214407-edward-webapp</i>.
- In you Git Bash terminal, run `python -m venv env` to create the virtual environment, followed by `source ./env/bin/activate` to activate the virtual environment.
- To install the dependencies to run the website, run `pip install -r requirements.txt`.
- With that, to run the RESTful API tests, run `python -m pytest tests/test_api.py -p no:randomly -v`.
- To run the application tests, run `python -m pytest tests/test_application.py --randomly-seed=14 -v`

<b>Model links on Render.com:</b>
- Conv2D for 128x128 images: https://ca2-dl-models.onrender.com/v1/models/conv2d128
- CustomVGG for 31x31 images: https://ca2-dl-models.onrender.com/v1/models/customvgg31 

<b>Branches:</b>

- Main => Main Repository

REPOSITORY: CA2-DAAA2B04-2214407-EDWARD

- DLApp-Model-Branch => Issue #1, Issue #2

REPOSITORY: CA2-DAAA2B04-2214407-EDWARD-WEBAPP

- DLApp-WebApp-Branch => Issue #3, Issue #4, Issue #14, Issue #15, Issue #8

- DLApp-BackEnd-Branch => Issue #6, Issue #7

- DLApp-Testing-Branch => Issue #9, Issue #10, Issue #11

- DLApp-Deployment-Branch => Issue #12, Issue #13

Total issues: 14

Total branches including main: 6

*The issues & scrumboard can be found in the `CA2-DAAA2B04-2214407-EDWARD` GitLab repository, which can be found <a href='https://gitlab.com/2b04.2214407.edwardtan/ca2-daaa2b04-2214407-edward'>Here</a>.

<b>Docker Containers:</b>

- CA2_Models_Server => Model Development

- CA2_Models_Serving => TensorFlow Serving

- CA2_Web_Server => Web Application & Development

<b>Docker Networks:</b>

- ca2_dl_network => Connects CA2_Models_Sever & CA2_Models_Serving

🤓 Thank you for visiting!
