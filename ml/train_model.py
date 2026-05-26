import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


# Dummy starter dataset
data = pd.DataFrame({
    "income": [20000, 30000, 40000, 50000, 25000, 60000, 15000, 70000],
    "fixed_expenses": [12000, 15000, 18000, 20000, 14000, 22000, 10000, 26000],
    "daily_avg": [500, 450, 600, 700, 550, 800, 400, 900],
    "savings_rate": [0.10, 0.15, 0.20, 0.18, 0.08, 0.25, 0.05, 0.30],
    "risk": [1, 0, 0, 0, 1, 0, 1, 0]
})

X = data[[
    "income",
    "fixed_expenses",
    "daily_avg",
    "savings_rate"
]]

y = data["risk"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

os.makedirs("ml", exist_ok=True)

joblib.dump(
    model,
    "ml/overspending_model.pkl"
)

print("Model saved successfully.")