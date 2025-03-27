from app.models.ml_models import (
    LogisticRegressionModel,
    DecisionTreeModel,
    RandomForestModel,
    load_data,
)


class ModelManager:
    def __init__(self):
        # Load and train models initially
        self.X_train, self.X_test, self.y_train, self.y_test = load_data()
        if self.X_train is None or self.y_train is None:
            raise RuntimeError("Failed to load training data.")

        self.available_models = {
            "logistic_regression": LogisticRegressionModel(),
            "decision_tree": DecisionTreeModel(),
            "random_forest": RandomForestModel(),
        }

        # Train the models
        for model in self.available_models.values():
            model.fit(self.X_train, self.y_train)

        # Default model
        self.current_model = self.available_models["logistic_regression"]

    def switch_model(self, model_name: str):
        """Switch the active model."""
        if model_name not in self.available_models:
            return {"status": "error", "message": f"Model '{model_name}' is not available."}, 400  # Return error with status code

        self.current_model = self.available_models[model_name]
        return {"status": "success", "message": f"Model switched to {model_name}"}, 200  # Return success with status code

    def get_current_model(self):
        """Get the current active model."""
        return {"current_model": self.current_model.__class__.__name__}

    def get_available_models(self):
        """Get a list of available models."""
        return list(self.available_models.keys())