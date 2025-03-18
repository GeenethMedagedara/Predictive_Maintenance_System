"""
Handles anomaly detection using Isolation Forest.
"""

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    """Detects anomalies in time-series data using Isolation Forest."""
    def __init__(self, model_path="../notebooks/models/isolation_forest.pkl", contamination=0.0015, random_state=7):
        self.model_path = model_path
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(n_estimators=100, contamination=self.contamination, random_state=self.random_state)
    
    def fit_predict(self, data: pd.DataFrame, feature_column: str):
        """Fits the model and predicts anomalies."""
        self.model.fit(data[[feature_column]])
        data["anomaly_score"] = self.model.predict(data[[feature_column]])
        data["anomaly"] = data["anomaly_score"].apply(lambda x: 1 if x == -1 else 0)
        
        # Save the trained model
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")
        
        return data
    
    def load_model(self):
        """Loads the trained model."""
        self.model = joblib.load(self.model_path)
        print(f"Model loaded from {self.model_path}")
    
    def plot_anomalies(self, data: pd.DataFrame, feature_column: str):
        """Plots anomalies detected by the model."""
        plt.figure(figsize=(20, 10))
        plt.plot(data.index, data[feature_column], label="EC2 Value", color="blue")
        plt.scatter(data.index[data["anomaly"] == 1], data[feature_column][data["anomaly"] == 1], color="red", label="Anomalies")
        plt.legend()
        plt.title("Anomaly Detection with Isolation Forest")
        plt.show()
