"""
Handles Autoencoder model for anomaly detection
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import joblib
import matplotlib.pyplot as plt

class AutoencoderAnomalyDetector:
    """Autoencoder for anomaly detection using Strategy Pattern"""

    def __init__(self, encoding_dim=32):
        self.encoding_dim = encoding_dim
        self.autoencoder = None

    def build_autoencoder(self, input_dim):
        """Builds the autoencoder model"""
        input_layer = Input(shape=(input_dim,))
        encoder = Dense(self.encoding_dim, activation='relu')(input_layer)
        decoder = Dense(input_dim, activation='sigmoid')(encoder)
        autoencoder = Model(inputs=input_layer, outputs=decoder)
        return autoencoder

    def train(self, data_train, save_model_path="../notebooks/models/autoencoder.h5"):
        """Trains Autoencoder model for anomaly detection"""
        X = data_train['value_normalized'].values.reshape(-1, 1)  # Reshape to (samples, features)
        input_dim = X.shape[1]

        self.autoencoder = self.build_autoencoder(input_dim)
        self.autoencoder.compile(optimizer='adam', loss='mse')

        self.autoencoder.fit(X, X, epochs=50, batch_size=32, validation_split=0.2)

        # Save trained model
        self.autoencoder.save(save_model_path)
        print(f"Autoencoder model saved at {save_model_path}")

        return self.autoencoder

    def detect_anomalies(self, data_test, threshold_percentile=99.85):
        """Detects anomalies using the trained autoencoder"""
        z = data_test['value_normalized'].values.reshape(-1, 1)
        predictions = self.autoencoder.predict(z)

        # Compute reconstruction error (MSE)
        mse = np.mean(np.power(z - predictions, 2), axis=1)

        # Set threshold based on percentile
        threshold = np.percentile(mse, threshold_percentile)
        data_test['autoencoder_anomaly'] = (mse > threshold).astype(int)

        return data_test, mse, threshold

    def plot_anomalies(self, data_test):
        """Plots detected anomalies"""
        plt.figure(figsize=(12, 5))
        plt.plot(data_test.index, data_test['value_normalized'], label='Value Normalized')
        plt.scatter(data_test.index[data_test['autoencoder_anomaly'] == 1],
                    data_test['value_normalized'][data_test['autoencoder_anomaly'] == 1],
                    color='red', label='Autoencoder Anomalies')
        plt.legend()
        plt.title('Autoencoder Anomaly Detection')
        plt.show()

# Context class for strategy pattern
class AnomalyDetectionContext:
    """Context class to use different anomaly detection strategies"""
    
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_training(self, data_train):
        return self.strategy.train(data_train)

    def execute_detection(self, data_test):
        return self.strategy.detect_anomalies(data_test)