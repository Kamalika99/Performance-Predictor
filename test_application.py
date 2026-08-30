"""
Starter test suite for application.py

Run from the project root with:
    pytest test_application.py -v

Place this file in a `tests/` folder (recommended) or the project root.
If you move it into tests/, make sure tests/__init__.py exists OR run
pytest from the project root so `application` is importable (it is,
since application.py sits at the root next to setup.py).
"""

import pytest
import application as app_module


@pytest.fixture
def client():
    app_module.application.config.update(TESTING=True)
    with app_module.application.test_client() as client:
        yield client


# A full, valid form submission matching the actual data.csv schema.
VALID_FORM_DATA = {
    'school': 'GP',
    'sex': 'F',
    'age': '17',
    'address': 'U',
    'famsize': 'GT3',
    'Pstatus': 'T',
    'Medu': '3',
    'Fedu': '2',
    'Mjob': 'services',
    'Fjob': 'other',
    'reason': 'course',
    'guardian': 'mother',
    'traveltime': '1',
    'studytime': '2',
    'failures': '0',
    'schoolsup': 'no',
    'famsup': 'yes',
    'paid': 'no',
    'activities': 'yes',
    'nursery': 'yes',
    'higher': 'yes',
    'internet': 'yes',
    'romantic': 'no',
    'famrel': '4',
    'freetime': '3',
    'goout': '3',
    'Dalc': '1',
    'Walc': '1',
    'health': '5',
    'absences': '4',
    'G1': '12',
    'G2': '13',
}


# ---------------------------------------------------------------------
# Basic route availability
# ---------------------------------------------------------------------

def test_index_route_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_predictdata_get_returns_200(client):
    response = client.get('/predictdata')
    assert response.status_code == 200


# ---------------------------------------------------------------------
# Input validation on POST /predictdata
# ---------------------------------------------------------------------

def test_predictdata_post_missing_fields_shows_error(client):
    # Send an incomplete form (no fields at all).
    response = client.post('/predictdata', data={})
    assert response.status_code == 200
    assert b"Missing required field" in response.data


def test_predictdata_post_non_numeric_values_rejected(client):
    form_data = dict(VALID_FORM_DATA)
    form_data['absences'] = 'not-a-number'

    response = client.post('/predictdata', data=form_data)
    assert response.status_code == 200
    assert b"must contain whole numbers" in response.data


# ---------------------------------------------------------------------
# Happy path, with the model pipeline mocked out.
#
# We don't want unit tests depending on a trained model artifact being
# present on disk. Monkeypatching PredictPipeline lets us test the
# Flask route logic in isolation from the ML pipeline.
# ---------------------------------------------------------------------

def test_predictdata_post_valid_input_returns_prediction(client, monkeypatch):
    class FakePredictPipeline:
        def predict(self, pred_df):
            return [12.5]

    monkeypatch.setattr(app_module, 'PredictPipeline', FakePredictPipeline)

    response = client.post('/predictdata', data=VALID_FORM_DATA)
    assert response.status_code == 200
    assert b"12.5" in response.data


def test_predictdata_post_pipeline_exception_is_handled_gracefully(client, monkeypatch):
    class FailingPredictPipeline:
        def predict(self, pred_df):
            raise RuntimeError("model file not found")

    monkeypatch.setattr(app_module, 'PredictPipeline', FailingPredictPipeline)

    response = client.post('/predictdata', data=VALID_FORM_DATA)
    # Should not 500 - the route's try/except should catch it and
    # render a friendly error message instead.
    assert response.status_code == 200
    assert b"Something went wrong" in response.data
