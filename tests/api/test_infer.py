from unittest.mock import Mock, patch
import numpy as np
import pytest
from fastapi.testclient import TestClient
import builtins

mock_model = Mock()
mock_model.predict.return_value = np.array([1])

def mock_verify_factory(scope):
    async def _verify(credentials=None):
        return "mock-token"
    return _verify

original_open = builtins.open

def selective_mock_open(file, *args, **kwargs):
    if "model.pkl" in str(file):
        mock_file = Mock()
        mock_file.__enter__ = Mock(return_value=mock_file)
        mock_file.__exit__ = Mock(return_value=False)
        return mock_file
    return original_open(file, *args, **kwargs)

with (
    patch("builtins.open", side_effect=selective_mock_open),
    patch("pickle.load", return_value=mock_model),
    patch("titanic.api.infer.verify_token", mock_verify_factory),
):
    from titanic.api.infer import app

@pytest.fixture(autouse=True)
def reset_oauth_env():
    import os
    with patch.dict(os.environ, {"OAUTH2_DOMAIN": ""}, clear=False):
        yield

@pytest.fixture
def mock_infer_model():
    model = Mock()
    model.predict.return_value = np.array([1])
    with patch("titanic.api.infer.model", model):
        yield model

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_infer_first_class_female(client, mock_infer_model):
    mock_infer_model.predict.return_value = np.array([1])
    payload = {"pclass": 1, "sex": "female", "sibSp": 0, "parch": 0}
    response = client.post("/infer", json=payload, headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    assert response.json() == [1]

def test_infer_third_class_male(client, mock_infer_model):
    mock_infer_model.predict.return_value = np.array([0])
    payload = {"pclass": 3, "sex": "male", "sibSp": 0, "parch": 0}
    response = client.post("/infer", json=payload, headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    assert response.json() == [0]

def test_infer_without_token(client):
    payload = {"pclass": 1, "sex": "female", "sibSp": 0, "parch": 0}
    response = client.post("/infer", json=payload)
    assert response.status_code == 401

def test_infer_invalid_pclass(client):
    payload = {"pclass": 5, "sex": "female", "sibSp": 0, "parch": 0}
    response = client.post("/infer", json=payload, headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 422

def test_infer_invalid_sex(client):
    payload = {"pclass": 1, "sex": "unknown", "sibSp": 0, "parch": 0}
    response = client.post("/infer", json=payload, headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 422
