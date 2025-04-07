import pytest

from app.core.model_manager import load_data  # Ensure this loads the real data
from app.models.ml_models import (
    DecisionTreeModel,
    LogisticRegressionModel,
    RandomForestModel,
)

# Load the real dataset (features and success rate)
X_train, X_test, y_train, y_test = load_data()


@pytest.fixture
def models():
    return {
        "logistic_regression": LogisticRegressionModel(),
        "decision_tree": DecisionTreeModel(),
        "random_forest": RandomForestModel(),
    }


def test_logistic_regression_fit(models):
    model = models["logistic_regression"]
    model.fit(X_train, y_train)
    assert (
        model.predict(X_test).shape[0] == y_test.shape[0]
    ), "Prediction output shape mismatch"


def test_decision_tree_fit(models):
    model = models["decision_tree"]
    model.fit(X_train, y_train)
    assert (
        model.predict(X_test).shape[0] == y_test.shape[0]
    ), "Prediction output shape mismatch"


def test_random_forest_fit(models):
    model = models["random_forest"]
    model.fit(X_train, y_train)
    assert (
        model.predict(X_test).shape[0] == y_test.shape[0]
    ), "Prediction output shape mismatch"
