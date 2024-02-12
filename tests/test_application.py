# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: test_application.py
# ==================================================
# EXPECTED RESULTS: 31 PASSED, 19 XFAILED
# ==================================================

# Import modules
from application.models import Entry
import pytest
from bs4 import BeautifulSoup
import base64
import json
import pickle

# Get labels
with open("labels.pickle", "rb") as file:
    labels = pickle.load(file)
    for key, value in labels.items():
        new_value = value.replace("_", " ")
        labels[key] = new_value

# CSRFTokenManager class
class CSRFTokenManager:
    # Function to get CSRF token of given route
    @staticmethod
    def get_csrf(client, route):
        # Get CSRF token to allow form validation as Flask-WTForms have CSRF protection enabled for forms by default
        get_resp = client.get(route)
        soup = BeautifulSoup(get_resp.data, "html.parser")
        csrf_token = soup.find("input", {"name": "csrf_token"})["value"]
        return csrf_token


# ==============================
# Convert image to base64 format
# ==============================
def image_to_b64(image_path):
    with open(image_path, "rb") as img:
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
    @pytest.mark.parametrize(
        "url, expected_content",
        [
            ("/login", b"LOGIN"),
            ("/index", b"VEGETABLE CLASSIFIER"),
            ("/home", b"VEGETABLE CLASSIFIER"),
            ("/random-prediction-image", b"base64_image"),
            ("/predict", b"VEGETABLE CLASSIFIER"),
            ("/about", b"WHAT IS VEGG.AI?"),
            ("/more", b"WHAT IS VEGG.AI?"),
        ],
    )
    def test_navigation(client, url, expected_content):
        response = client.get(url)
        assert response.status_code == 200
        assert expected_content in response.data


# ===========
# Login Tests
# ===========
class TestLogin:
    @staticmethod
    def check_error_message(response, expected_error_message):
        soup = BeautifulSoup(response.data, "html.parser")
        err_msg = soup.find(string=expected_error_message)
        assert err_msg is not None
        assert response.status_code == 200

    @staticmethod
    def perform_login(client, email, password, csrf_token):
        return client.post(
            "/login",
            data={"email": email, "password": password, "csrf_token": csrf_token},
            follow_redirects=True,
        )

    # Testing for login [EXPECTED FAILURE TESTING]
    # Check for:
    # - Incorrect login credentials
    # - Missing login credentials
    #       - Username
    #       - Password
    def test_login_incorrect(self, client):
        # Get CSRF token
        csrf_token = CSRFTokenManager.get_csrf(client=client, route="/login")
        # Incorrect login credentials
        response = self.perform_login(client, "admin@gmail.com", "ABC123", csrf_token)
        self.check_error_message(response, "Incorrect Credentials.")
        # Missing login credentials [USERNAME]
        response = self.perform_login(client, "", "123ABC", csrf_token)
        self.check_error_message(response, "This input is required.")
        # Missing login credentials [PASSWORD]
        response = self.perform_login(client, "admin@gmail.com", "", csrf_token)
        self.check_error_message(response, "This input is required.")

    # Testing for Login [VALIDITY TESTING]
    # Check for:
    # - Correct login credentials
    @staticmethod
    def test_login_correct(client):
        # Get CSRF token
        csrf_token = CSRFTokenManager.get_csrf(client=client, route="/login")
        response = client.post(
            "/login",
            data={
                "email": "admin@gmail.com",
                "password": "PassWord123",
                "csrf_token": csrf_token,
            },
            follow_redirects=True,
        )
        soup = BeautifulSoup(response.data, "html.parser")
        route_check = soup.find(string="VEGETABLE CLASSIFIER")
        assert route_check is not None
        assert response.status_code == 200


# ================
# Prediction Tests
# ================
class TestPrediction:
    @staticmethod
    def post_prediction(client, entry, convert=True):
        """Perform a POST request to the prediction API endpoint."""
        return client.post(
            "/predict",
            data=json.dumps(
                {
                    "image": image_to_b64(entry[0]) if convert else entry[0],
                    "image_size": entry[1],
                    "file_name": entry[2],
                }
            ),
            headers={"Content-Type": "application/json"},
            follow_redirects=True,
        )

    # SUCCESSFUL PREDICTIONS [VALIDITY TESTING]
    # Check that:
    # - The prediction works
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.parametrize(
        "entry_list",
        [
            ["./prediction-testing-images/0001.jpg", 128, "0001.jpg"],
            ["./prediction-testing-images/0001.jpg", 31, "0001.jpg"],
            ["./prediction-testing-images/0022.jpg", 128, "0022.jpg"],
            ["./prediction-testing-images/0142.jpg", 31, "0142.jpg"],
            ["./prediction-testing-images/0034.jpg", 128, "0034.jpg"],
            ["./prediction-testing-images/0052.jpg", 31, "0052.jpg"],
            ["./prediction-testing-images/0022.jpg", 31, "0022.jpg"],
            ["./prediction-testing-images/0142.jpg", 128, "0142.jpg"],
            ["./prediction-testing-images/0034.jpg", 31, "0034.jpg"],
            ["./prediction-testing-images/0052.jpg", 128, "0052.jpg"],
        ],
    )
    def test_prediction_valid(self, entry_list, client):
        """Test prediction with valid inputs"""
        response = self.post_prediction(client=client, entry=entry_list)
        assert response.data.decode("utf-8") in labels.values()
        assert response.status_code == 200

    # INCORRECT PREDICTIONS [UNEXPECTED FAILURE TESTING]
    # Check that:
    # - The prediction will NOT work for incorrect images and image sizes
    # - There is no need to check for file name as it is not processed, only displayed
    # - Unexpected failure as these are values not expected to be able to be inputted by users (as they are not options)
    # - Marked as "xfail" as we expect them to fail
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.xfail(reason="Incorrect image, or incorrect image size")
    @pytest.mark.parametrize(
        "entry_list",
        [
            ["notabase64imagelink", 128, "test_1.jpg"],
            ["realimage", 33, "test_14.jpg"],
            ["realimage", 13, "test_0.jpg"],
            ["hellllo", 1004, "test_54.jpg"],
            ["testing", 256, "test_27.jpg"],
            ["thiswontwork", 512, "test_99.jpg"],
            ["example1", 1024, "test_100.jpg"],
            ["example2", 2048, "test_101.jpg"],
            ["example3", 4096, "test_102.jpg"],
        ],
    )
    def test_prediction_invalid(self, entry_list, client):
        if entry_list[0] == "realimage":
            entry_list[0] = image_to_b64("./prediction-testing-images/0051.jpg")
        response = self.post_prediction(client=client, entry=entry_list, convert=False)
        # Should return False so that xfail is raised correctly as we expect these to fail (should return response code of 500 as these should NOT pass)
        assert response.status_code == 200

    # CONSISTENT PREDICTIONS 31x31 and 128x128 [CONSISTENCY TESTING]
    # Check that:
    # - Given same inputs, the predicted price remains the same
    def check_consistent_predictions(self, client, image_path, image_size):
        previous_prediction = None
        loops = 3
        data = json.dumps(
            {
                "image": image_to_b64(image_path),
                "image_size": image_size,
            }
        )
        for _ in range(loops):
            response = client.post(
                "/predict",
                data=data,
                headers={"Content-Type": "application/json"},
                follow_redirects=True,
            )
            current_prediction = response.data.decode("utf-8")
            if previous_prediction is not None:
                assert (
                    current_prediction == previous_prediction
                ), "Inconsistent predictions detected."
            previous_prediction = current_prediction

    # TEST FOR 128X128
    @pytest.mark.filterwarnings("ignore")
    def test_prediction_consistent_128(self, client):
        self.check_consistent_predictions(
            client, "./prediction-testing-images/0051.jpg", 128
        )

    # TEST FOR 31X31
    @pytest.mark.filterwarnings("ignore")
    def test_prediction_consistent_31(self, client):
        self.check_consistent_predictions(
            client, "./prediction-testing-images/0023.jpg", 31
        )


# =============
# Backend Tests
# =============
class TestBackEnd:
    # HISTORY ENTRY [VALIDITY TESTING]
    # Check that:
    # - History entry constraints are working
    # - History entry does not interfere with values
    # - The history entry can be made
    @pytest.mark.parametrize(
        "entry_list",
        [
            ["0001.jpg", "./prediction-testing-images/0001.jpg", 128, "Cabbage"],
            ["0001.jpg", "./prediction-testing-images/0001.jpg", 31, "Cabbage"],
            ["0022.jpg", "./prediction-testing-images/0022.jpg", 128, "Brinjal"],
            ["0142.png", "./prediction-testing-images/0142.jpg", 31, "Tomato"],
            ["0034.jpg", "./prediction-testing-images/0034.jpg", 128, "Bean"],
            ["0052.jpg", "./prediction-testing-images/0052.jpg", 31, "Potato"],
            ["0022.png", "./prediction-testing-images/0022.jpg", 31, "Brinjal"],
            ["0142.jpg", "./prediction-testing-images/0142.jpg", 128, "Tomato"],
            ["0034.jpg", "./prediction-testing-images/0034.jpg", 31, "Bean"],
            ["0052.png", "./prediction-testing-images/0052.jpg", 128, "Potato"],
        ],
    )
    def test_history(self, entry_list):
        file_name, image_path, image_size, prediction = entry_list

        # Create Entry object
        new_entry = Entry(
            file_name=file_name,
            image=image_to_b64(image_path),
            image_size=image_size,
            prediction=prediction,
        )

        # Assert values and constraints
        assert new_entry.file_name == file_name
        assert new_entry.image == image_to_b64(image_path)
        assert new_entry.image_size in (128, 31)
        assert new_entry.prediction in labels.values()
        assert new_entry.file_name.endswith(".png") or new_entry.file_name.endswith(
            ".jpg"
        )

    # INVALID HISTORY ENTRY [UNEXPECTED FAILURE TESTING]
    # Check that:
    # - History entry constraints correctly validate against incorrect values trying to be passed in
    # - Unexpected failure as these are values not expected to be able to be inputted by users (as they are validate/not options)
    @pytest.mark.xfail(
        reason="Invalid inputs (file name, image blob, image size or prediction)"
    )
    @pytest.mark.parametrize(
        "entry_list",
        [
            ["0001.webp", "./prediction-testing-images/0001.jpg", 128, "Cabbage"],
            ["0001.pdf", "./prediction-testing-images/0001.jpg", 31, "Cabbage"],
            ["0022.jpg", "./prediction-testing-images/0022.jpg", 1028, "Brinjal"],
            ["0142.jpg", "./prediction-testing-images/0142.jpg", 10004, "Tomato"],
            ["0034.jpg", "./prediction-testing-images/0034.jpg", 128, "Cake"],
            ["0052.jpg", ".imnotanimagehehe", 31, "Potato"],
            ["0022.csv", "./prediction-testing-images/0022.jpg", 31, "Brinjal"],
            ["0142.py", "./prediction-testing-images/0142.jpg", 128, "Tomato"],
            ["0034.jpg", ".imdefinitelyanimagelol", 31, "Bean"],
            ["0052.jpg", "./prediction-testing-images/0052.jpg", 128, "Salad"],
        ],
    )
    def test_history_invalid(self, entry_list):
        self.test_history(entry_list=entry_list)
