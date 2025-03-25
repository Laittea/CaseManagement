from app.models.ml_models import LogisticRegressionModel, DecisionTreeModel, RandomForestModel, load_data

class ModelManager:
    def __init__(self):
        # Load and train models initially
        self.X_train, self.X_test, self.y_train, self.y_test = load_data()
        self.available_models = {
            "logistic_regression": LogisticRegressionModel(),
            "decision_tree": DecisionTreeModel(),
            "random_forest": RandomForestModel()
        }

        # Train the models
        for model in self.available_models.values():
            model.fit(self.X_train, self.y_train)

        # Default model
        self.current_model = self.available_models["logistic_regression"]

    def switch_model(self, model_name: str):
        """Switch the active model."""
        if model_name in self.available_models:
            self.current_model = self.available_models[model_name]
            return {"status": "success", "message": f"Model switched to {model_name}"}
        else:
            return {"status": "error", "message": "Model not available."}

    def get_current_model(self):
        """Get the current active model."""
        return {"current_model": self.current_model.__class__.__name__}

    def get_available_models(self):
        """Get a list of available models."""
        return {"available_models": list(self.available_models.keys())}