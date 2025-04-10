import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from app.database import SessionLocal
from app.models import Client, ClientCase


class MLModel:
    """Base class for machine learning models."""

    def fit(self, X_train, y_train):
        pass

    def predict(self, X_test):
        pass


class LogisticRegressionModel(MLModel):
    def __init__(self):
        self.model = LogisticRegression(max_iter=200)

    def fit(self, X_train, y_train):
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise ValueError(
                f"Error during model fitting in LogisticRegressionModel: {e}"
            )

    def predict(self, X_test):
        try:
            return self.model.predict(X_test)
        except Exception as e:
            raise ValueError(
                f"Error during model prediction in LogisticRegressionModel: {e}"
            )


class DecisionTreeModel(MLModel):
    def __init__(self):
        self.model = DecisionTreeClassifier(random_state=42)

    def fit(self, X_train, y_train):
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise ValueError(f"Error during model fitting in DecisionTreeModel: {e}")

    def predict(self, X_test):
        try:
            return self.model.predict(X_test)
        except Exception as e:
            raise ValueError(f"Error during model prediction in DecisionTreeModel: {e}")


class RandomForestModel(MLModel):
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def fit(self, X_train, y_train):
        try:
            self.model.fit(X_train, y_train)
        except Exception as e:
            raise ValueError(f"Error during model fitting in RandomForestModel: {e}")

    def predict(self, X_test):
        try:
            return self.model.predict(X_test)
        except Exception as e:
            raise ValueError(f"Error during model prediction in RandomForestModel: {e}")


def load_data():
    """Load and split the client and case data for training/testing."""
    # Create a session to interact with the database
    db = SessionLocal()

    # Query all clients and their case data (success_rate from ClientCase)
    clients = db.query(Client).all()
    client_cases = db.query(ClientCase).all()

    # Check if data exists
    if not clients or not client_cases:
        db.close()
        raise ValueError("No client or case data found in the database.")

    # Prepare the features (X) and target (y)
    X = []
    y = []

    # Loop over each client and their corresponding case
    for client, case in zip(clients, client_cases):
        X.append(
            [
                client.age,
                client.work_experience,
                client.canada_workex,
                client.level_of_schooling,
                client.fluent_english,
                client.reading_english_scale,
                client.speaking_english_scale,
                client.writing_english_scale,
                client.numeracy_scale,
                client.computer_scale,
                client.transportation_bool,
                client.caregiver_bool,
                client.housing,
                client.income_source,
                client.felony_bool,
                client.attending_school,
                client.currently_employed,
                client.substance_use,
                client.time_unemployed,
                client.need_mental_health_support_bool,
            ]
        )

        # Success rate is the target variable
        y.append(case.success_rate)

    # Convert to numpy arrays for model compatibility
    X = np.array(X)
    y = np.array(y)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    db.close()  # Always close the session after using it
    return X_train, X_test, y_train, y_test
