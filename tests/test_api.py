# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: test_api.py
# ==================================================
# EXPECTED RESULT: 49 PASSED, 11 XFAILED
# ==================================================

# Import modules
from tests.test_application import image_to_b64
import pytest
import json

# ==============================================================================
# ! PLEASE REMEMBER TO RUN WITH -p no:randomly IF PYTEST-RANDOMLY IS INSTALLED !
# ==============================================================================

# =================
# RESTful API Tests
# =================
class TestRESTful:
    """Tests for RESTful APIs in the application"""

    @staticmethod
    def add_post(client, data):
        """Return client post for add API"""
        return client.post(
            "/api/add",
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True,
        )

    @staticmethod
    def format_data(entry):
        """Format data dictionary"""
        return {
            "file_name": entry[0],
            "image": image_to_b64(entry[1]),
            "image_size": entry[2],
            "prediction": entry[3],
        }

    @staticmethod
    def post_user(client, email, username, password):
        """Return client post for sign up API"""
        return client.post(
            "/api/signup",
            data=json.dumps(
                {"email": email, "username": username, "password": password}
            ),
            content_type="application/json",
            follow_redirects=True,
        )

    @staticmethod
    def assert_response(response):
        response_body = json.loads(response.get_data(as_text=True))
        # Assert statements
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response_body["id"]

    # Unit testing for Signup API [VALIDITY TESTING]
    # Check that:
    # - The sign up works for users that provide valid inputs
    @pytest.mark.parametrize(
        "entry_list",
        [
            ["a@gmail.com", "user1", "ABCDefGE"],
            ["hznneyang@gmail.com", "zhnyang", "qweqeQRQIQ"],
            ["achary@gmail.com", "dario", "qwrihbEBI"],
            ["drrrarro@gmail.com", "zachary", "fonwfibEFIBW"],
        ],
    )
    def test_signup_api_valid(self, client, entry_list):
        """Test signup API"""
        response = self.post_user(client, entry_list[0], entry_list[1], entry_list[2])
        self.assert_response(response)

    # Unit testing for Signup API [EXPECTED FAILURE TESTING]
    # Check that:
    # - The sign up works for users that provide valid inputs
    @pytest.mark.xfail(reason="Invalid inputs")
    @pytest.mark.parametrize(
        "entry_list",
        [
            ["a@gmail.com", "", "ABCDefGE"],
            ["achary@gmail.com", "", "qwrihbEBI"],
            ["drrrarro@gmail.com", "zachary", "fonw"],
        ],
    )
    def test_signup_api_invalid(self, client, entry_list):
        """Test signup API"""
        response = self.post_user(client, entry_list[0], entry_list[1], entry_list[2])
        self.assert_response(response)

    # Unit testing for add API [VALIDITY TESTING]
    # Check that:
    # - The table constraints allow valid values from being added
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
    def test_add_api_valid(self, client, entry_list):
        """Test add entry API with valid inputs"""
        response = self.add_post(client=client, data=self.format_data(entry_list))
        self.assert_response(response)

    # Unit testing for add API [EXPECTED FAILURE TESTING]
    # Check that:
    # - The table constraints do prevent incorrect values from being added
    # - Utilize err.log to verify that the table constraint check failed
    @pytest.mark.xfail(reason="Incorrect file name, image, image size or prediction")
    @pytest.mark.parametrize(
        "entry_list",
        [
            ["0001", "./prediction-testing-images/0001.jpg", 31, "Pumpkin"],
            ["0001.png", "./prediction-testing-images/0001.jpg", -100, "Pumpkin"],
            ["0001.webp", "./prediction-testing-images/0001.jpg", 31, "Pumpkin"],
            ["0001.jpg", "./prediction-testing-images/0001.jpg", 128, "Mcspicy"],
            ["0001.jpg", "", 128, "Cucumber"],
            ["", "./prediction-testing-images/0001.jpg", 31, "Pumpkin"],
            ["0001.jpg", "./prediction-testing-images/0001.jpg", 1000, "Mcspicy"],
            ["0001.jpg", "./prediction-testing-images/0001.jpg", -128, "Cucumber"],
        ],
    )
    def test_add_api_invalid(self, client, entry_list):
        """Test add entry API with invalid inputs"""
        response = self.add_post(client=client, data=self.format_data(entry_list))
        # Assert statements
        # These should also FAIL as the table constraints should prevent the values from being added, hence these checks should return FALSE for xfail flag to be correctly shown
        self.assert_response(response)

    # Unit testing for get API [VALIDITY TESTING]
    @pytest.mark.parametrize(
        "entry_id, file_name, image_path, image_size, prediction",
        [
            [1, "0001.jpg", "./prediction-testing-images/0001.jpg", 128, "Cabbage"],
            [2, "0001.jpg", "./prediction-testing-images/0001.jpg", 31, "Cabbage"],
            [3, "0022.jpg", "./prediction-testing-images/0022.jpg", 128, "Brinjal"],
            [4, "0142.png", "./prediction-testing-images/0142.jpg", 31, "Tomato"],
            [5, "0034.jpg", "./prediction-testing-images/0034.jpg", 128, "Bean"],
            [6, "0052.jpg", "./prediction-testing-images/0052.jpg", 31, "Potato"],
            [7, "0022.png", "./prediction-testing-images/0022.jpg", 31, "Brinjal"],
            [8, "0142.jpg", "./prediction-testing-images/0142.jpg", 128, "Tomato"],
            [9, "0034.jpg", "./prediction-testing-images/0034.jpg", 31, "Bean"],
            [10, "0052.png", "./prediction-testing-images/0052.jpg", 128, "Potato"],
        ],
    )
    def test_get_api(
        self, client, entry_id, file_name, image_path, image_size, prediction
    ):
        """Test get API"""
        # Test the get API
        response = client.get(f"/api/get/{entry_id}")
        response_body = json.loads(response.get_data(as_text=True))
        # Assert statements
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response_body["id"] == entry_id
        assert response_body["file_name"] == file_name
        assert "base64," in response_body["image"]
        assert response_body["image_size"] == image_size
        assert response_body["prediction"] == prediction

    # Unit testing for delete API [VALIDITY TESTING]
    @staticmethod
    @pytest.mark.parametrize(
        "entry_list", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    )
    def test_delete_api(client, entry_list):
        """Test delete API"""
        response = client.post(f"/api/delete/{entry_list}")
        assert response.status_code == 200
        assert json.loads(response.get_data(as_text=True))["result"] == "Success"

    # Testing to check if delete API actually removed all the entries [VALIDITY TESTING]
    @staticmethod
    def test_empty_history(client):
        """Test empty history to ensure all entries were removed"""
        response = client.get("/api/get_all")
        history = json.loads(response.get_data(as_text=True))
        assert history == []

    # Unit testing for predict API [VALIDITY TESTING]
    @staticmethod
    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.parametrize(
        "entry_list",
        [
            ["./prediction-testing-images/0001.jpg", 128, "Cabbage"],
            ["./prediction-testing-images/0001.jpg", 31, "Cabbage"],
            ["./prediction-testing-images/0022.jpg", 128, "Brinjal"],
            ["./prediction-testing-images/0142.jpg", 31, "Tomato"],
            ["./prediction-testing-images/0034.jpg", 128, "Bean"],
            ["./prediction-testing-images/0052.jpg", 31, "Potato"],
            ["./prediction-testing-images/0022.jpg", 31, "Brinjal"],
            ["./prediction-testing-images/0142.jpg", 128, "Tomato"],
            ["./prediction-testing-images/0034.jpg", 31, "Bean"],
            ["./prediction-testing-images/0052.jpg", 128, "Potato"],
        ],
    )
    def test_prediction_valid(client, entry_list):
        """Test prediction API with valid inputs"""
        data = {
            "image": image_to_b64(entry_list[0]),
            "image_size": entry_list[1],
        }
        response = client.post(
            "/api/predict",
            data=json.dumps(data),
            content_type="application/json",
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert (
            json.loads(response.get_data(as_text=True))["prediction"] == entry_list[2]
        )
