import os
import sys

import dill
from sklearn.metrics import r2_score

from src.mlproject.exception import CustomException


def save_object(file_path, obj):
    """Save a Python object to disk using dill."""
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    """Load a Python object previously saved with save_object."""
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models: dict):
    """
    Fit each candidate regression model, evaluate it on the test set with
    R2 score and return a {model_name: test_r2_score} report.
    """
    try:
        report = {}

        for model_name, model in models.items():
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
