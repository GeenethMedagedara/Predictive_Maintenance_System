"""
Handles data preprocessing and normalization.
"""

import os
import joblib
from sklearn.preprocessing import MinMaxScaler, StandardScaler

class NormalizationStrategy:
    """Base class for normalization strategies."""
    def normalize(self, data):
        raise NotImplementedError("Subclasses must implement normalize method")
    
    def save_scaler(self, file_path):
        """Saves the fitted scaler to a file."""
        joblib.dump(self.scaler, file_path)
        print(f"✅ Scaler saved to {file_path}")

class MinMaxNormalization(NormalizationStrategy):
    """MinMax Scaling Normalization."""
    def __init__(self):
        self.scaler = MinMaxScaler()

    def normalize(self, data):
        return self.scaler.fit_transform(data)

class StandardNormalization(NormalizationStrategy):
    """Standard Scaling Normalization (Z-score)."""
    def __init__(self):
        self.scaler = StandardScaler()

    def normalize(self, data):
        return self.scaler.fit_transform(data)

class DataPreprocessor:
    """Applies a chosen normalization strategy to the dataset."""
    def __init__(self, strategy: NormalizationStrategy, save_path="../notebooks/scaler_data/scaler.pkl"):
        self.strategy = strategy
        self.save_path = save_path
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

    def apply_normalization(self, data, column):
        data[column + '_normalized'] = self.strategy.normalize(data[[column]])
        
        # ✅ Save the fitted scaler
        self.strategy.save_scaler(self.save_path)
        return data