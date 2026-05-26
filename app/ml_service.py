import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


MODEL_PATH = "ml/overspending_model.pkl"


class MLService:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.model = None

    def train_dummy_model(self):
        # Simple starter model for demo/project base
        data = pd.DataFrame({
            "income": [20000, 30000, 40000, 50000, 25000, 60000, 15000, 70000],
            "fixed_expenses": [12000, 15000, 18000, 20000, 14000, 22000, 10000, 26000],
            "daily_avg": [500, 450, 600, 700, 550, 800, 400, 900],
            "savings_rate": [0.10, 0.15, 0.20, 0.18, 0.08, 0.25, 0.05, 0.30],
            "risk": [1, 0, 0, 0, 1, 0, 1, 0]
        })

        X = data[["income", "fixed_expenses", "daily_avg", "savings_rate"]]
        y = data["risk"]

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(model, self.model_path)
        self.model = model

    def predict_risk(self, income, fixed_expenses, daily_avg, savings_rate):
        if self.model is None:
            self.train_dummy_model()

        features = np.array([[income, fixed_expenses, daily_avg, savings_rate]])
        pred = self.model.predict(features)[0]
        prob = self.model.predict_proba(features)[0].max()

        if pred == 1:
            label = "High Overspending Risk"
        else:
            label = "Low Overspending Risk"

        return label, float(prob)

    def safety_net(self, monthly_essential_spend):
        return monthly_essential_spend * 6