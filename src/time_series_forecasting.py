"""
Handles time-series forecasting using LSTM.
"""

import numpy as np
import joblib
import tensorflow as tf
import matplotlib.pyplot as plt

class ForecastingStrategy:
    """Base class for different forecasting strategies."""
    def forecast(self, data):
        raise NotImplementedError("Subclasses must implement forecast method")
    
    def plot_forecast(self, y_test, y_pred):
        """Plots actual vs predicted values."""
        plt.figure(figsize=(12, 5))
        plt.plot(y_test, label="Actual EC2 Readings", color="blue")
        plt.plot(y_pred, label="Predicted EC2 Readings", color="red")
        plt.legend()
        plt.title("Time-Series Forecasting")
        plt.show()

class LSTMForecaster(ForecastingStrategy):
    """LSTM-based time-series forecaster."""
    def __init__(self, model_path="../notebooks/models/lstm_model.h5", scaler_path="../notebooks/scaler_data/scaler.pkl", time_steps_path="../notebooks/models/time_steps.pkl"):
        self.model = tf.keras.models.load_model(model_path, compile=False)
        self.model.compile(optimizer="adam", loss=tf.keras.losses.MeanSquaredError())
        
        self.scaler = joblib.load(scaler_path)
        self.time_steps = joblib.load(time_steps_path)
    
    def forecast(self, data):
        """Generates predictions using the trained LSTM model."""
        X_test, y_test = self.create_sequences(data["value_normalized"].values)
        X_test = X_test.reshape((-1, self.time_steps, 1))
        
        y_pred = self.model.predict(X_test)
        
        y_test_rescaled = self.scaler.inverse_transform(y_test.reshape(-1, 1))
        y_pred_rescaled = self.scaler.inverse_transform(y_pred.reshape(-1, 1))
        
        return y_test_rescaled, y_pred_rescaled, y_pred
    
    def create_sequences(self, data):
        """Creates sequences for LSTM model."""
        X, y = [], []
        for i in range(len(data) - self.time_steps):
            X.append(data[i:i + self.time_steps])
            y.append(data[i + self.time_steps])
        return np.array(X), np.array(y)

class ForecastingContext:
    """Context class for applying different forecasting strategies."""
    def __init__(self, strategy: ForecastingStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: ForecastingStrategy):
        self.strategy = strategy
    
    def run_forecast(self, data):
        return self.strategy.forecast(data)
    
    def plot_results(self, y_test, y_pred):
        self.strategy.plot_forecast(y_test, y_pred)