import app.services
import app.services.user_service
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import pandas as pd

client = TestClient(app)

def test_create_target_users_success():
    # Data to be sent to the API
    request_data = {
        "user_data": {
            "gender": "Male",
            "occupation": ["Engineer"],
            "city": ["Milan", "Roma"],
            "income": [50000, 100000],
            "age": [25, 35],
            "interest": {
                "interests": ["Technology", "Fashion"],
                "weights": [0.7, 0.3]
            },
            "n_users": 50,
            "confidence_level": "High"
        }
    }
    # Mock the dependencies
    with patch('app.utils.data_manager.get_data') as mock_get_data, \
         patch('app.services.user_service.process_user_data') as mock_process_user_data:

        # Setup mock returns
        mock_get_data.return_value = {'data': pd.DataFrame()}
        mock_process_user_data.return_value = pd.DataFrame()

        # Make the request to the endpoint
        response = client.post("/target-users/", json=request_data)

        # Assertions
        assert response.status_code == 200


def test_create_target_users_failure():
    request_data = {
        "user_data": {
            "gender": "Male",
            "occupation": ["Engineer"],
            "city": ["Milan", "Roma"],
            "income": [50000, 100000],
            "age": [25, 35],
            "interest": {
                "interests": ["Technology", "Fashion"],
                "weights": [0.7, 0.3]
            },
            "n_users": 50,
            "confidence_level": "High"
        }
    }

    # Mock the dependencies
    with patch('app.utils.data_manager.get_data') as mock_get_data, \
         patch('app.services.user_service.process_user_data') as mock_process_user_data:

        # Setup mock returns
        mock_get_data.return_value = {'data': pd.DataFrame()}
        mock_process_user_data.return_value = None 

        response = client.post("/target-users/", json=request_data)

        # Assertions
        assert response.status_code == 500
        assert response.json() == {"message": "No result"}