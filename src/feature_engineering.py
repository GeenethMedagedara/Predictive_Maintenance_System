"""
Handles feature engineering for time-series data.
"""

import pandas as pd
import numpy as np
from scipy.fftpack import fft
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.ensemble import IsolationForest

class FeatureEngineering:
    def __init__(self, data):
        """
        Initialize FeatureEngineering with the dataset.
        :param data: Pandas DataFrame containing time-series data.
        """
        self.data = data

    def normalize_column(self, column):
        """
        Normalize a column using MinMaxScaler.
        """
        scaler = MinMaxScaler()
        self.data[f"{column}_normalized"] = scaler.fit_transform(self.data[[column]])
    
    def add_statistical_features(self, column, window=10):
        """
        Add statistical features: mean, std deviation, skewness, kurtosis.
        """
        self.data[f"{column}_mean"] = self.data[column].rolling(window=window, min_periods=1).mean()
        self.data[f"{column}_std_dev"] = self.data[column].rolling(window=window, min_periods=1).std()
        self.data[f"{column}_skewness"] = self.data[column].rolling(window=window, min_periods=1).skew()
        self.data[f"{column}_kurtosis"] = self.data[column].rolling(window=window, min_periods=1).kurt()

    def add_rolling_features(self, column, window=5):
        """
        Add rolling window features: mean, max, min.
        """
        self.data[f"{column}_rolling_mean"] = self.data[column].rolling(window=window, min_periods=1).mean()
        self.data[f"{column}_rolling_max"] = self.data[column].rolling(window=window, min_periods=1).max()
        self.data[f"{column}_rolling_min"] = self.data[column].rolling(window=window, min_periods=1).min()

    def add_fourier_features(self, column):
        """
        Perform Fourier Transform and extract real & imaginary components.
        """
        fft_values = fft(self.data[column].values)
        self.data[f"{column}_fft_real"] = np.real(fft_values)
        self.data[f"{column}_fft_imag"] = np.imag(fft_values)

    def add_lag_features(self, column, lags=3):
        """
        Create lag features to capture past values.
        """
        for lag in range(1, lags + 1):
            self.data[f"{column}_lag_{lag}"] = self.data[column].shift(lag)

    def add_time_features(self, datetime_column):
        """
        Extract time-based features from timestamp.
        """
        self.data[datetime_column] = pd.to_datetime(self.data[datetime_column])
        self.data["hour"] = self.data[datetime_column].dt.hour
        self.data["day"] = self.data[datetime_column].dt.day
        self.data["month"] = self.data[datetime_column].dt.month
        self.data["weekday"] = self.data[datetime_column].dt.weekday

    def add_anomaly_scores(self, column):
        """
        Use Isolation Forest to detect anomalies.
        """
        iso_forest = IsolationForest(n_estimators=100, contamination=0.0015, random_state=42)
        self.data["anomaly_score"] = iso_forest.fit_predict(self.data[[column]])
        self.data["anomaly"] = self.data["anomaly_score"].apply(lambda x: 1 if x == -1 else 0)

    def add_categorical_encoding(self, column):
        """
        Perform both Label Encoding & One-Hot Encoding.
        """
        label_encoder = LabelEncoder()
        self.data[f"{column}_encoded"] = label_encoder.fit_transform(self.data[column])

        onehot_encoder = OneHotEncoder(sparse=False)
        onehot_encoded = onehot_encoder.fit_transform(self.data[[column]])
        onehot_df = pd.DataFrame(onehot_encoded, columns=[f"{column}_{i}" for i in range(onehot_encoded.shape[1])])
        
        self.data = self.data.join(onehot_df)

    def add_spike_detection(self, column, threshold=3):
        """
        Detect sudden spikes or drops in the time-series data.
        """
        self.data["spike"] = (self.data[column].diff().abs() > threshold).astype(int)

    def apply_all_features(self, column, datetime_column=None):
        """
        Apply all feature engineering techniques to the dataset.
        """
        # self.normalize_column(column)
        self.add_statistical_features(column)
        self.add_rolling_features(column)
        self.add_fourier_features(column)
        self.add_lag_features(column, lags=3)
        # self.add_anomaly_scores(column)
        if datetime_column:
            self.add_time_features(datetime_column)
        return self.data
