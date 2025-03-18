"""
Handles the backend API for the Anomaly Detection application.
"""

import os
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from flask_cors import CORS
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_file
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)

CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": [
            "http://host.docker.internal:8080",
            "http://localhost:8080",
            "http://backend:4000"  # If using Docker Compose
        ],
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }
})

# Load Pretrained Models
lstm_model = load_model("../notebooks/models/lstm_model.h5", compile=False)
lstm_model.compile(optimizer="adam", loss="mse")

autoencoder = load_model("../notebooks/models/autoencoder.h5", compile=False)
autoencoder.compile(optimizer="adam", loss="mse")

# Load Scalers & Configs
scaler = joblib.load("../notebooks/scaler_data/scaler.pkl")
time_steps = joblib.load("../notebooks/models/time_steps.pkl")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def create_sequences(data, time_steps):
    """Helper function to create LSTM input sequences."""
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])
        y.append(data[i + time_steps])
    return np.array(X), np.array(y)

def detect_anomalies(data):
    """Runs Autoencoder & LSTM on the data and flags anomalies."""
    
    # Normalize Data
    data["value_normalized"] = scaler.transform(data["value"].values.reshape(-1, 1))

    # LSTM Forecasting
    X_test, _ = create_sequences(data["value_normalized"].values, time_steps)
    X_test = X_test.reshape((-1, time_steps, 1))
    y_pred = lstm_model.predict(X_test)

    # Restore original scale
    y_pred_rescaled = scaler.inverse_transform(y_pred.reshape(-1, 1))
    y_thresh = y_pred_rescaled.flatten()  # Convert to 1D for thresholding

    # Define Threshold for Predicted Failures (95th percentile)
    threshold = np.percentile(y_thresh, 95)
    data["predicted_failure"] = (data["value_normalized"] > threshold).astype(int)

    # Autoencoder Anomaly Detection
    X_auto = data["value_normalized"].values.reshape(-1, 1)
    predictions = autoencoder.predict(X_auto)
    mse = np.mean(np.power(X_auto - predictions, 2), axis=1)
    
    # Set anomaly threshold (99.85 percentile)
    autoencoder_threshold = np.percentile(mse, 99.85)
    data["autoencoder_anomaly"] = (mse > autoencoder_threshold).astype(int)

    # Final Maintenance Alert Column (Combining Both Models)
    data["maintenance_alert"] = data["autoencoder_anomaly"] | data["predicted_failure"]

    return data

def plot_results(data, filename):
    """Plots the results with detected anomalies."""
    plt.figure(figsize=(12, 5))
    plt.plot(data.index, data["value"], label="Sensor Readings", color="blue")
    
    # Highlight Maintenance Alerts
    plt.scatter(
        data.index[data["maintenance_alert"] == 1],
        data["value"][data["maintenance_alert"] == 1],
        color="red",
        label="Maintenance Alert (Autoencoder & LSTM)",
        marker="x",
    )
    
    plt.legend()
    plt.title("Anomaly Detection with Autoencoder & LSTM")
    plt.xlabel("Timestamp")
    plt.ylabel("Sensor Readings")
    plt.savefig(filename)
    plt.close()

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles CSV file upload, processes data, and returns the anomaly visualization."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Load CSV & Preprocess Data
        data = pd.read_csv(filepath, parse_dates=["timestamp"])
        data.set_index("timestamp", inplace=True)

        # Run Anomaly Detection
        processed_data = detect_anomalies(data)

        # Generate Visualization
        output_image = "output/anomaly_detection.png"
        plot_results(processed_data, output_image)

        return send_file(output_image, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000,debug=True)
