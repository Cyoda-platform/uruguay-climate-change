"""LSTM model for temperature forecasting."""

import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import joblib


class LSTMTemperatureForecaster:
    """LSTM-based temperature forecasting model."""

    def __init__(self, lookback=60, forecast_horizon=30):
        """
        Initialize LSTM forecaster.

        Args:
            lookback: Number of past days to use for prediction
            forecast_horizon: Number of days to forecast
        """
        self.lookback = lookback
        self.forecast_horizon = forecast_horizon
        self.model = None
        self.scaler = MinMaxScaler()

    def create_sequences(self, data):
        """
        Create sequences for LSTM training.

        Args:
            data: Time series data

        Returns:
            X, y arrays for training
        """
        X, y = [], []
        for i in range(len(data) - self.lookback - self.forecast_horizon + 1):
            X.append(data[i:i + self.lookback])
            y.append(data[i + self.lookback:i + self.lookback + self.forecast_horizon])
        return np.array(X), np.array(y)

    def build_model(self, input_shape):
        """
        Build LSTM model architecture.

        Args:
            input_shape: Shape of input data

        Returns:
            Compiled Keras model
        """
        model = Sequential([
            LSTM(128, activation='relu', return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(64, activation='relu', return_sequences=True),
            Dropout(0.2),
            LSTM(32, activation='relu'),
            Dropout(0.2),
            Dense(self.forecast_horizon)
        ])

        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        return model

    def train(self, temperature_data, epochs=100, batch_size=32, validation_split=0.2):
        """
        Train LSTM model.

        Args:
            temperature_data: Array or Series of temperature values
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_split: Validation data split ratio

        Returns:
            Training history
        """
        # Scale data
        scaled_data = self.scaler.fit_transform(temperature_data.reshape(-1, 1)).flatten()

        # Create sequences
        X, y = self.create_sequences(scaled_data)

        # Reshape for LSTM [samples, timesteps, features]
        X = X.reshape(X.shape[0], X.shape[1], 1)

        # Build model
        self.model = self.build_model((X.shape[1], 1))

        # Early stopping
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )

        # Train
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stop],
            verbose=1
        )

        return history

    def predict(self, recent_data, steps=30):
        """
        Make multi-step forecast.

        Args:
            recent_data: Recent temperature data (last lookback days)
            steps: Number of steps to forecast

        Returns:
            Forecasted values with confidence intervals
        """
        if self.model is None:
            raise ValueError("Model not trained yet!")

        # Scale input
        scaled_input = self.scaler.transform(recent_data.reshape(-1, 1)).flatten()

        # Prepare input sequence
        input_seq = scaled_input[-self.lookback:].reshape(1, self.lookback, 1)

        # Predict
        predictions = []
        for _ in range(steps // self.forecast_horizon + 1):
            pred = self.model.predict(input_seq, verbose=0)
            predictions.extend(pred[0])

            # Update sequence for next prediction
            if len(predictions) < steps:
                input_seq = np.append(input_seq[:, 1:, :],
                                     pred.reshape(1, -1, 1)[:, :self.lookback-1, :],
                                     axis=1)

        predictions = predictions[:steps]

        # Inverse scale
        predictions = self.scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)
        ).flatten()

        # Calculate confidence intervals (simplified)
        std_dev = np.std(predictions) * 0.5
        lower_bound = predictions - 2 * std_dev
        upper_bound = predictions + 2 * std_dev

        return predictions, lower_bound, upper_bound

    def save_model(self, model_path, scaler_path):
        """Save model and scaler."""
        self.model.save(model_path)
        joblib.dump(self.scaler, scaler_path)

    def load_model(self, model_path, scaler_path):
        """Load model and scaler."""
        self.model = keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
