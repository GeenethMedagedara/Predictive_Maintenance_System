"""
Handles evaluation of the model and plotting of anomalies.
"""

from sklearn.metrics import precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import numpy as np

def evaluate_model(y_true, y_pred):
    """Computes precision, recall, and F1-score."""
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1}")
    
    return precision, recall, f1

def plot_anomaly_comparison(data, y_true, y_pred, value_column='value_normalized'):
    """Plots true vs predicted anomalies."""
    plt.figure(figsize=(20, 10))
    plt.plot(data.index, data[value_column], label=value_column)
    
    plt.scatter(data.index[y_true == 1],
                data[value_column][y_true == 1],
                color='red', label='True Anomalies')
    
    plt.scatter(data.index[y_pred == 1],
                data[value_column][y_pred == 1],
                color='lightgreen', alpha=0.3, label='Predicted Anomalies')
    
    plt.legend()
    plt.title("Anomaly Detection: True vs Predicted")
    plt.show()