"""Prophet model for seasonal analysis and forecasting."""

import pandas as pd
import numpy as np
from prophet import Prophet
import joblib


class ProphetSeasonalAnalyzer:
    """Prophet-based seasonal analysis and forecasting."""

    def __init__(self, yearly_seasonality=True, weekly_seasonality=False,
                 daily_seasonality=False):
        """
        Initialize Prophet analyzer.

        Args:
            yearly_seasonality: Include yearly seasonality
            weekly_seasonality: Include weekly seasonality
            daily_seasonality: Include daily seasonality
        """
        self.model = Prophet(
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=weekly_seasonality,
            daily_seasonality=daily_seasonality,
            interval_width=0.95
        )
        self.fitted = False

    def train(self, df, date_column='date', value_column='value'):
        """
        Train Prophet model.

        Args:
            df: DataFrame with date and value columns
            date_column: Name of date column
            value_column: Name of value column

        Returns:
            Fitted model
        """
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df[date_column]),
            'y': df[value_column]
        })

        # Fit model
        self.model.fit(prophet_df)
        self.fitted = True

        return self.model

    def forecast(self, periods=365, freq='D'):
        """
        Generate forecast.

        Args:
            periods: Number of periods to forecast
            freq: Frequency ('D' for daily, 'M' for monthly, etc.)

        Returns:
            DataFrame with forecast and components
        """
        if not self.fitted:
            raise ValueError("Model not trained yet!")

        # Create future dataframe
        future = self.model.make_future_dataframe(periods=periods, freq=freq)

        # Generate forecast
        forecast = self.model.predict(future)

        return forecast

    def get_components(self, forecast):
        """
        Extract seasonal components.

        Args:
            forecast: Forecast DataFrame from Prophet

        Returns:
            Dictionary with trend and seasonal components
        """
        components = {
            'trend': forecast[['ds', 'trend']].to_dict('records'),
            'yearly': forecast[['ds', 'yearly']].to_dict('records') if 'yearly' in forecast.columns else None,
            'weekly': forecast[['ds', 'weekly']].to_dict('records') if 'weekly' in forecast.columns else None,
        }

        return components

    def detect_anomalies(self, df, date_column='date', value_column='value', threshold=0.05):
        """
        Detect anomalies using Prophet's uncertainty intervals.

        Args:
            df: DataFrame with actual data
            date_column: Name of date column
            value_column: Name of value column
            threshold: Threshold for anomaly detection

        Returns:
            DataFrame with anomalies marked
        """
        if not self.fitted:
            raise ValueError("Model not trained yet!")

        # Get forecast for historical period
        forecast = self.forecast(periods=0)

        # Merge with actual data
        df_with_forecast = df.copy()
        df_with_forecast['ds'] = pd.to_datetime(df_with_forecast[date_column])

        merged = df_with_forecast.merge(
            forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
            on='ds',
            how='left'
        )

        # Mark anomalies
        merged['is_anomaly'] = (
            (merged[value_column] < merged['yhat_lower']) |
            (merged[value_column] > merged['yhat_upper'])
        )

        merged['anomaly_score'] = np.abs(merged[value_column] - merged['yhat'])

        return merged

    def get_forecast_summary(self, forecast, last_n=30):
        """
        Get summary of forecast.

        Args:
            forecast: Forecast DataFrame
            last_n: Number of recent predictions to return

        Returns:
            Dictionary with forecast summary
        """
        recent_forecast = forecast.tail(last_n)

        summary = {
            'predictions': recent_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records'),
            'trend_direction': 'increasing' if forecast['trend'].iloc[-1] > forecast['trend'].iloc[-last_n] else 'decreasing',
            'mean_prediction': float(recent_forecast['yhat'].mean()),
            'uncertainty_range': float(recent_forecast['yhat_upper'].mean() - recent_forecast['yhat_lower'].mean())
        }

        return summary

    def save_model(self, filepath):
        """Save Prophet model."""
        joblib.dump(self.model, filepath)

    def load_model(self, filepath):
        """Load Prophet model."""
        self.model = joblib.load(filepath)
        self.fitted = True
