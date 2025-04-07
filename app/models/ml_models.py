import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from app.database import SessionLocal
from app.models import Client, ClientCase


class MLModel:
    """Base class for machine learning models."""

    def fit(self, features_train, targets_train):
        raise NotImplementedError

    def predict(self, features_test):
        raise NotImplementedError


class LogisticRegressionModel(MLModel):
    def __init__(self):
        self.model = LogisticRegression(max_iter=200)

    def fit(self, features_train, targets_train):
        try:
            self.model.fit(features_train, targets_train)
        except Exception as error:
            raise ValueError(
                f"Error during model fitting in LogisticRegressionModel: {error}"
            )

    def predict(self, features_test):
        try:
            return self.model.predict(features_test)
        except Exception as error:
            raise ValueError(
                f"Error during model prediction in LogisticRegressionModel: {error}"
            )


class DecisionTreeModel(MLModel):
    def __init__(self):
        self.model = DecisionTreeClassifier(random_state=42)

    def fit(self, features_train, targets_train):
        try:
            self.model.fit(features_train, targets_train)
        except Exception as error:
            raise ValueError(
                f"Error during model fitting in DecisionTreeModel: {error}"
            )

    def predict(self, features_test):
        try:
            return self.model.predict(features_test)
        except Exception as error:
            raise ValueError(
                f"Error during model prediction in DecisionTreeModel: {error}"
            )


class RandomForestModel(MLModel):
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)

    def fit(self, features_train, targets_train):
        try:
            self.model.fit(features_train, targets_train)
        except Exception as error:
            raise ValueError(
                f"Error during model fitting in RandomForestModel: {error}"
            )

    def predict(self, features_test):
        try:
            return self.model.predict(features_test)
        except Exception as error:
            raise ValueError(
                f"Error during model prediction in RandomForestModel: {error}"
            )


def load_and_split_client_data():
    """
    Load and split the client and case data for training/testing.
    """
    db = SessionLocal()

    client_records = db.query(Client).all()
    client_case_records = db.query(ClientCase).all()

    if not client_records or not client_case_records:
        db.close()
        raise ValueError("No client or case data found in the database.")

    features = []
    targets = []

    for client, case in zip(client_records, client_case_records):
        features.append(
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
        targets.append(case.success_rate)

    features = np.array(features)
    targets = np.array(targets)

    features_train, features_test, targets_train, targets_test = train_test_split(
        features, targets, test_size=0.3, random_state=42
    )

    db.close()
    return features_train, features_test, targets_train, targets_test
