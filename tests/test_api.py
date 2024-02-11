# ==================================================
# ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
# NAME: EDWARD TAN YUAN CHONG
# CLASS: DAAA/FT/2B/04
# ADM NO: 2214407
# ==================================================
# FILENAME: test_api.py
# ==================================================
# EXPECTED RESULT: 45 PASSED, 5 XFAILED
# ==================================================

# Import modules
from tests.test_application import image_to_b64
import pytest
import json

# =================
# RESTful API Tests
# =================
class TestRESTful:
    # Unit testing for add API [VALIDITY TESTING]
    # Check that:
    # - The table constraints allow valid values from being added
    @classmethod
    @pytest.mark.parametrize('entry_list',[
        {'file_name': '0001.jpg', 'image': image_to_b64('./prediction-testing-images/0001.jpg'), 'image_size': 128, 'prediction': 'Cabbage'},
        {'file_name': '0001.jpg', 'image': image_to_b64('./prediction-testing-images/0001.jpg'), 'image_size': 31, 'prediction': 'Cabbage'},
        {'file_name': '0022.jpg', 'image': image_to_b64('./prediction-testing-images/0022.jpg'), 'image_size': 128, 'prediction': 'Brinjal'},
        {'file_name': '0142.png', 'image': image_to_b64('./prediction-testing-images/0142.jpg'), 'image_size': 31, 'prediction': 'Tomato'},
        {'file_name': '0034.jpg', 'image': image_to_b64('./prediction-testing-images/0034.jpg'), 'image_size': 128, 'prediction': 'Bean'},
        {'file_name': '0052.jpg', 'image': image_to_b64('./prediction-testing-images/0052.jpg'), 'image_size': 31, 'prediction': 'Potato'},
        {'file_name': '0022.png', 'image': image_to_b64('./prediction-testing-images/0022.jpg'), 'image_size': 31, 'prediction': 'Brinjal'},
        {'file_name': '0142.jpg', 'image': image_to_b64('./prediction-testing-images/0142.jpg'), 'image_size': 128, 'prediction': 'Tomato'},
        {'file_name': '0034.jpg', 'image': image_to_b64('./prediction-testing-images/0034.jpg'), 'image_size': 31, 'prediction': 'Bean'},
        {'file_name': '0052.png', 'image': image_to_b64('./prediction-testing-images/0052.jpg'), 'image_size': 128, 'prediction': 'Potato'}
    ])
    def test_add_api(self,client,entry_list):
        response = client.post('/api/add',data=json.dumps(entry_list),content_type="application/json", follow_redirects=True)
        # Assert statements
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"]

    # Unit testing for add API [EXPECTED FAILURE TESTING]
    # Check that:
    # - The table constraints do prevent incorrect values from being added
    # - Utilize err.log to verify that the table constraint check failed
    @classmethod
    @pytest.mark.xfail(reason='Incorrect file name, image, image size or prediction')
    @pytest.mark.parametrize('entry_list',[
        {'file_name': '0001', 'image': image_to_b64('./prediction-testing-images/0001.jpg'), 'image_size': 31, 'prediction': 'Pumpkin'},
        {'file_name': '0001.png', 'image': image_to_b64('./prediction-testing-images/0001.jpg'), 'image_size': -100, 'prediction': 'Pumpkin'},
        {'file_name': '0001.webp', 'image': image_to_b64('./prediction-testing-images/0001.jpg'), 'image_size': 31, 'prediction': 'Pumpkin'},
        {'file_name': '0001.jpg', 'image': image_to_b64('./prediction-testing-images/0001.jpg'), 'image_size': 128, 'prediction': 'Mcspicy'},
        {'file_name': '0001.jpg', 'image': '', 'image_size': 128, 'prediction': 'Cucumber'},
    ])
    def test_add_api_incorrect(self,client,entry_list):
        response = client.post('/api/add',data=json.dumps(entry_list),content_type="application/json", follow_redirects=True)
        # Assert statements
        response_body = json.loads(response.get_data(as_text=True))
        # These should also FAIL as the table constraints should prevent the values from being added, hence these checks should return FALSE for xfail flag to be correctly shown
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response_body["id"]

    # Unit testing for get API
    @classmethod
    @pytest.mark.parametrize('entry_list',[
        [1, '0001.jpg', './prediction-testing-images/0001.jpg', 128, 'Cabbage'],
        [2, '0001.jpg', './prediction-testing-images/0001.jpg', 31, 'Cabbage'],
        [3, '0022.jpg', './prediction-testing-images/0022.jpg', 128, 'Brinjal'],
        [4, '0142.png', './prediction-testing-images/0142.jpg', 31, 'Tomato'],
        [5, '0034.jpg', './prediction-testing-images/0034.jpg', 128, 'Bean'],
        [6, '0052.jpg', './prediction-testing-images/0052.jpg', 31, 'Potato'],
        [7, '0022.png', './prediction-testing-images/0022.jpg', 31, 'Brinjal'],
        [8, '0142.jpg', './prediction-testing-images/0142.jpg', 128, 'Tomato'],
        [9, '0034.jpg', './prediction-testing-images/0034.jpg', 31, 'Bean'],
        [10, '0052.png', './prediction-testing-images/0052.jpg', 128, 'Potato']
    ])
    def test_get_api(self,client,entry_list):
        # Test the get API
        response = client.get(f'/api/get/{entry_list[0]}')
        response_body = json.loads(response.get_data(as_text=True))
        # Assert statements
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        assert response_body['id'] == entry_list[0]
        assert response_body['file_name'] == entry_list[1]
        assert "base64," in response_body['image']
        assert response_body['image_size'] == entry_list[3]
        assert response_body['prediction'] == entry_list[4]

    # Unit testing for delete API
    @staticmethod
    @pytest.mark.parametrize('entry_list',[
        1,2,3,4,5,6,7,8,9,10,11,12,13,14
    ])
    def test_delete_api(client,entry_list):
        response = client.post(f"/api/delete/{entry_list}")
        assert response.status_code == 200
        assert json.loads(response.get_data(as_text=True))['result'] == 'Success'

    # Testing to check if delete API actually removed all the entries
    @staticmethod
    def test_empty_history(client):
        response = client.get("/api/get")
        history = json.loads(response.get_data(as_text=True))
        assert history == []

    # Unit testing for predict API
    @staticmethod
    @pytest.mark.filterwarnings('ignore')
    @pytest.mark.parametrize('entry_list',[
        {'image': image_to_b64('./prediction-testing-images/0001.jpg'), 'image_size': 128, 'prediction': 'Cabbage'},
        {'image': image_to_b64('./prediction-testing-images/0001.jpg'), 'image_size': 31, 'prediction': 'Cabbage'},
        {'image': image_to_b64('./prediction-testing-images/0022.jpg'), 'image_size': 128, 'prediction': 'Brinjal'},
        {'image': image_to_b64('./prediction-testing-images/0142.jpg'), 'image_size': 31, 'prediction': 'Tomato'},
        {'image': image_to_b64('./prediction-testing-images/0034.jpg'), 'image_size': 128, 'prediction': 'Bean'},
        {'image': image_to_b64('./prediction-testing-images/0052.jpg'), 'image_size': 31, 'prediction': 'Potato'},
        {'image': image_to_b64('./prediction-testing-images/0022.jpg'), 'image_size': 31, 'prediction': 'Brinjal'},
        {'image': image_to_b64('./prediction-testing-images/0142.jpg'), 'image_size': 128, 'prediction': 'Tomato'},
        {'image': image_to_b64('./prediction-testing-images/0034.jpg'), 'image_size': 31, 'prediction': 'Bean'},
        {'image': image_to_b64('./prediction-testing-images/0052.jpg'), 'image_size': 128, 'prediction': 'Potato'}
    ])
    def test_prediction(client, entry_list):
        response = client.post('/api/predict', 
                               data=json.dumps(entry_list),
                               content_type="application/json", 
                               follow_redirects=True
                               )
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert json.loads(response.get_data(as_text=True))['prediction'] == entry_list['prediction']