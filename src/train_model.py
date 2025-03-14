import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib

class LSTMTrainer:
    """LSTM model trainer using Strategy Pattern"""

    def __init__(self, time_steps=10):
        self.time_steps = time_steps
        self.model = None

    def create_sequences(self, data):
        """Creates sequences for LSTM input"""
        X, y = [], []
        for i in range(len(data) - self.time_steps):
            X.append(data[i:i + self.time_steps])
            y.append(data[i + self.time_steps])
        return np.array(X), np.array(y)

    def train(self, data_train, data_test, save_model_path="../notebooks/models/lstm_model.h5"):
        """Trains LSTM model on time-series data"""
        X_train, y_train = self.create_sequences(data_train["value_normalized"].values)
        X_test, y_test = self.create_sequences(data_test["value_normalized"].values)

        # Reshape for LSTM input
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        print(f"Training Data Shape: X_train: {X_train.shape}, y_train: {y_train.shape}")
        print(f"Testing Data Shape: X_test: {X_test.shape}, y_test: {y_test.shape}")

        # Build LSTM Model
        self.model = Sequential([
            LSTM(50, activation="relu", return_sequences=True, input_shape=(self.time_steps, 1)),
            Dropout(0.2),
            LSTM(50, activation="relu"),
            Dense(1)
        ])

        self.model.compile(optimizer="adam", loss="mse")

        self.model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test))

        # Save Model
        self.model.save(save_model_path)
        print(f"Model saved at {save_model_path}")
        joblib.dump(self.time_steps, "../notebooks/models/time_steps.pkl")

        return self.model

# Context class to switch between different training strategies (future extensibility)
class ModelTrainingContext:
    """Context class to use different training strategies"""
    
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_training(self, data_train, data_test):
        return self.strategy.train(data_train, data_test)