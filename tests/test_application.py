# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: test_application.py
# ==================================================
# EXPECTED RESULTS: 25 PASSED, 1 SKIPPED, 19 XFAILED
# ==================================================

# Import modules
from application.models import Entry
import pytest
from bs4 import BeautifulSoup
import base64
import json
import pickle

# Get labels
with open('labels.pickle','rb') as file:
    labels = pickle.load(file)
    for key,value in labels.items():
        new_value = value.replace('_',' ')
        labels[key] = new_value

# CSRFTokenManager class
class CSRFTokenManager:
    # Function to get CSRF token of given route
    @staticmethod
    def get_csrf(client, route):
        # Get CSRF token to allow form validation as Flask-WTForms have CSRF protection enabled for forms by default
        get_resp = client.get(route)
        soup = BeautifulSoup(get_resp.data, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        return csrf_token
    
# ==============================
# Convert image to base64 format
# ==============================
def image_to_b64(image_path):
    with open(image_path, 'rb') as img:
        encoded = base64.b64encode(img.read())
        encoded_string = f"data:image/jpeg;base64,{encoded.decode('utf-8')}"
    return encoded_string

# ===============
# Navigation Test
# ===============
class TestNavigation:
    # NAVIGATION TEST [VALIDITY TEST]
    # Check that:
    # - Website redirects user correctly
    @staticmethod
    def test_navigation(client):
        # LOGIN
        response = client.get('/login')
        assert response.status_code == 200
        assert b"LOGIN" in response.data

        # INDEX
        response = client.get('/index')
        assert response.status_code == 200
        assert b"VEGETABLE CLASSIFIER" in response.data

        response = client.get('/home')
        assert response.status_code == 200
        assert b"VEGETABLE CLASSIFIER" in response.data

        # PREDICT
        response = client.get('/predict')
        assert response.status_code == 200
        assert b"VEGETABLE CLASSIFIER" in response.data

        # ABOUT
        response = client.get('/about')
        assert response.status_code == 200
        assert b"WHAT IS VEGG.AI?" in response.data

# ===========
# Login Tests
# ===========
class TestLogin:
    # Testing for login [EXPECTED FAILURE TESTING]
    # Check for:
    # - Incorrect login credentials
    # - Missing login credentials
    #       - Username
    #       - Password
    @staticmethod
    def test_login_incorrect(client):
        # Get CSRF token
        csrf_token = CSRFTokenManager.get_csrf(client=client, route='/login') 
        # Incorrect login credentials
        response = client.post('/login',data={'username':'Admin123', 'password':'ABC123', 'csrf_token': csrf_token}, follow_redirects=True)
        soup = BeautifulSoup(response.data, 'html.parser')
        err_msg = soup.find(string='Incorrect Credentials.')
        assert err_msg is not None
        assert response.status_code == 200
        
        # Missing login credentials [USERNAME]
        response = client.post('/login',data={'username':'', 'password':'123ABC', 'csrf_token': csrf_token}, follow_redirects=True)
        soup = BeautifulSoup(response.data, 'html.parser')
        err_msg = soup.find(string='This input is required.')
        assert err_msg is not None
        assert response.status_code == 200

        # Missing login credentials [PASSWORD]
        response = client.post('/login',data={'username':'Admin', 'password':'', 'csrf_token': csrf_token}, follow_redirects=True)
        soup = BeautifulSoup(response.data, 'html.parser')
        err_msg = soup.find(string='This input is required.')
        assert err_msg is not None
        assert response.status_code == 200

    # Testing for Login [VALIDITY TESTING]
    # Check for:
    # - Correct login credentials
    @staticmethod
    def test_login_correct(client):
        # Get CSRF token
        csrf_token = CSRFTokenManager.get_csrf(client=client, route='/login') 
        response = client.post('/login',data={'username':'Admin', 'password':'123ABC', 'csrf_token': csrf_token}, follow_redirects=True)
        soup = BeautifulSoup(response.data, 'html.parser')
        route_check = soup.find(string='VEGETABLE CLASSIFIER')
        assert route_check is not None
        assert response.status_code == 200

# ================
# Prediction Tests
# ================
class TestPrediction:
    # SUCCESSFUL PREDICTIONS
    # Check that:
    # - The prediction works
    @pytest.mark.filterwarnings('ignore')
    @pytest.mark.parametrize('entry_list',[
        ["./prediction-testing-images/0001.jpg",128,'0001.jpg'],
        ["./prediction-testing-images/0001.jpg",31,'0001.jpg'],
        ["./prediction-testing-images/0022.jpg",128,'0022.jpg'],
        ["./prediction-testing-images/0142.jpg",31,'0142.jpg'],
        ["./prediction-testing-images/0034.jpg",128,'0034.jpg'],
        ["./prediction-testing-images/0052.jpg",31,'0052.jpg'],
        ["./prediction-testing-images/0022.jpg",31,'0022.jpg'],
        ["./prediction-testing-images/0142.jpg",128,'0142.jpg'],
        ["./prediction-testing-images/0034.jpg",31,'0034.jpg'],
        ["./prediction-testing-images/0052.jpg",128,'0052.jpg']
    ])
    def test_prediction(self,entry_list,client):
        response = client.post("/predict", 
            data=json.dumps({
                'image': image_to_b64(entry_list[0]),
                'image_size': entry_list[1],
                'file_name': entry_list[2]
            }, 
            separators=(',',':')),
            headers={'Content-Type': 'application/json'},
            follow_redirects=True)
        assert response.data.decode('utf-8') in labels.values()
        assert response.status_code == 200
    
    # INCORRECT PREDICTIONS [EXPECTED FAILURE TESTING]
    # Check that:
    # - The prediction will NOT work for incorrect images and image sizes
    # - There is no need to check for file name as it is not processed, only displayed
    # - Marked as "xfail" as we expect them to fail
    @classmethod
    @pytest.mark.filterwarnings('ignore')
    @pytest.mark.xfail(reason='Incorrect image, or incorrect image size')
    @pytest.mark.parametrize('entry_list', [
        ["notabase64imagelink",128,'test_1.jpg'],
        ["realimage",33,'test_14.jpg'],
        ["realimage",13,'test_0.jpg'],
        ["hellllo",1004,'test_54.jpg'],
        ["testing", 256, 'test_27.jpg'],
        ["thiswontwork", 512, 'test_99.jpg'],
        ["example1", 1024, 'test_100.jpg'],
        ["example2", 2048, 'test_101.jpg'],
        ["example3", 4096, 'test_102.jpg'],
    ]) 
    def test_prediction_incorrect(self,entry_list, client):
        if entry_list[0] == "realimage":
            entry_list[0] = image_to_b64("./prediction-testing-images/0051.jpg")
        response = client.post("/predict", 
                                data=json.dumps({
                                    'image': entry_list[0],
                                    'image_size': entry_list[1],
                                    'file_name': entry_list[2]
                                }),
                                headers={'Content-Type': 'application/json'}, 
                                follow_redirects=True)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Should return False so that xfail is raised correctly as we expect these to fail (should return response code of 500 as these should NOT pass)
        assert response.status_code == 200

    # CORRECT PREDICTIONS 31x31 [CONSISTENCY TESTING]
    # Check that:
    # - Given same inputs, the predicted price remains the same
    @pytest.mark.filterwarnings('ignore')
    def test_prediction_correct_31(self,client):
        previous_prediction = None
        loops = 3
        data = json.dumps({
                'image': image_to_b64("./prediction-testing-images/0142.jpg"),
                'image_size': 31,
                'file_name': '0142.jpg'
        })
        # Loops 3 times to compare predicted prices
        for _ in range(loops): 
            response = client.post("/predict", 
                                    data=data, 
                                    headers={'Content-Type': 'application/json'},
                                    follow_redirects=True)
            current_prediction = response.data.decode('utf-8')
            if previous_prediction is not None:
                assert current_prediction == previous_prediction, "Inconsistent predictions detected."
            previous_prediction = current_prediction

    # CORRECT PREDICTIONS 128x128 [CONSISTENCY TESTING]
    # Check that:
    # - Given same inputs, the predicted price remains the same
    @pytest.mark.skip(reason="Test is for other methods to use")
    def test_consistent_predictions(self, client, image_path, image_size):
        previous_prediction = None
        loops = 3
        data = json.dumps({
            'image': image_to_b64(image_path),
            'image_size': image_size,
        })
        for _ in range(loops):
            response = client.post("/predict",
                                   data=data,
                                   headers={'Content-Type': 'application/json'},
                                   follow_redirects=True)
            current_prediction = response.data.decode('utf-8')
            if previous_prediction is not None:
                assert current_prediction == previous_prediction, "Inconsistent predictions detected."
            previous_prediction = current_prediction

    # TEST FOR 128X128
    @pytest.mark.filterwarnings('ignore')
    def test_prediction_correct_128(self, client):
        self.test_consistent_predictions(client, "./prediction-testing-images/0051.jpg", 128)

    # TEST FOR 31X31
    @pytest.mark.filterwarnings('ignore')
    def test_prediction_correct_31(self, client):
        self.test_consistent_predictions(client, "./prediction-testing-images/0023.jpg", 31)


# =============
# Backend Tests
# =============
class TestBackEnd:
    # HISTORY ENTRY [VALIDITY TESTING]
    # Check that:
    # - History entry constraints are working
    # - History entry does not interfere with values
    # - The history entry can be made
    @classmethod
    @pytest.mark.parametrize('entry_list',[
        ['0001.jpg', './prediction-testing-images/0001.jpg', 128, 'Cabbage'],
        ['0001.jpg', './prediction-testing-images/0001.jpg', 31, 'Cabbage'],
        ['0022.jpg', './prediction-testing-images/0022.jpg', 128, 'Brinjal'],
        ['0142.png', './prediction-testing-images/0142.jpg', 31, 'Tomato'],
        ['0034.jpg', './prediction-testing-images/0034.jpg', 128, 'Bean'],
        ['0052.jpg', './prediction-testing-images/0052.jpg', 31, 'Potato'],
        ['0022.png', './prediction-testing-images/0022.jpg', 31, 'Brinjal'],
        ['0142.jpg', './prediction-testing-images/0142.jpg', 128, 'Tomato'],
        ['0034.jpg', './prediction-testing-images/0034.jpg', 31, 'Bean'],
        ['0052.png', './prediction-testing-images/0052.jpg', 128, 'Potato']
    ])
    def test_history(self,entry_list):
        new_entry = Entry(
            file_name = entry_list[0],
            image = image_to_b64(entry_list[1]),
            image_size= entry_list[2],
            prediction = entry_list[3]
        )
        # Checking the values are assigned correctly
        assert new_entry.file_name == entry_list[0]
        assert new_entry.image == image_to_b64(entry_list[1])
        assert new_entry.image_size == entry_list[2]
        assert new_entry.prediction == entry_list[3]

        # Checking entry constraints
        assert new_entry.prediction in labels.values()
        assert new_entry.image_size in (128,31)
        assert new_entry.file_name.endswith(".png") or new_entry.file_name.endswith('.jpg')

    # INVALID HISTORY ENTRY [EXPECTED FAILURE TESTING]
    # Check that:
    # - History entry constraints correctly validate against incorrect values trying to be passed in
    @classmethod
    @pytest.mark.xfail(reason='Invalid inputs (file name, image blob, image size or prediction)')
    @pytest.mark.parametrize('entry_list',[
        ['0001.webp', './prediction-testing-images/0001.jpg', 128, 'Cabbage'],
        ['0001.pdf', './prediction-testing-images/0001.jpg', 31, 'Cabbage'],
        ['0022.jpg', './prediction-testing-images/0022.jpg', 1028, 'Brinjal'],
        ['0142.jpg', './prediction-testing-images/0142.jpg', 10004, 'Tomato'],
        ['0034.jpg', './prediction-testing-images/0034.jpg', 128, 'Cake'],
        ['0052.jpg', '.imnotanimagehehe', 31, 'Potato'],
        ['0022.csv', './prediction-testing-images/0022.jpg', 31, 'Brinjal'],
        ['0142.py', './prediction-testing-images/0142.jpg', 128, 'Tomato'],
        ['0034.jpg', '.imdefinitelyanimagelol', 31, 'Bean'],
        ['0052.jpg', './prediction-testing-images/0052.jpg', 128, 'Salad']
    ])
    def test_history_invalid(self,entry_list):
        self.test_history(entry_list=entry_list)

