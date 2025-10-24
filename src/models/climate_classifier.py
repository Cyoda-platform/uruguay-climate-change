"""Climate pattern classification models."""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib


class ClimatePatternClassifier:
    """Classify climate patterns using Random Forest."""

    def __init__(self, n_estimators=100, random_state=42):
        """
        Initialize classifier.

        Args:
            n_estimators: Number of trees in the forest
            random_state: Random seed
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            max_depth=10,
            min_samples_split=5
        )
        self.fitted = False
        self.feature_names = None

    def create_climate_labels(self, df, temp_column='temperature',
                              precip_column='precipitation'):
        """
        Create climate pattern labels based on temperature and precipitation.

        Args:
            df: DataFrame with climate data
            temp_column: Name of temperature column
            precip_column: Name of precipitation column

        Returns:
            Series with climate pattern labels
        """
        # Calculate percentiles
        temp_25 = df[temp_column].quantile(0.33)
        temp_75 = df[temp_column].quantile(0.67)
        precip_25 = df[precip_column].quantile(0.33)
        precip_75 = df[precip_column].quantile(0.67)

        # Create labels
        labels = []
        for _, row in df.iterrows():
            temp = row[temp_column]
            precip = row[precip_column]

            if temp < temp_25 and precip < precip_25:
                label = 'Cold and Dry'
            elif temp < temp_25 and precip >= precip_75:
                label = 'Cold and Wet'
            elif temp >= temp_75 and precip < precip_25:
                label = 'Hot and Dry'
            elif temp >= temp_75 and precip >= precip_75:
                label = 'Hot and Wet'
            elif temp < temp_25:
                label = 'Cold and Moderate'
            elif temp >= temp_75:
                label = 'Hot and Moderate'
            elif precip < precip_25:
                label = 'Moderate and Dry'
            elif precip >= precip_75:
                label = 'Moderate and Wet'
            else:
                label = 'Moderate'

            labels.append(label)

        return pd.Series(labels, index=df.index)

    def prepare_features(self, df, temp_column='temperature',
                        precip_column='precipitation'):
        """
        Prepare features for classification.

        Args:
            df: DataFrame with climate data
            temp_column: Name of temperature column
            precip_column: Name of precipitation column

        Returns:
            Feature DataFrame
        """
        features = pd.DataFrame()

        # Current values
        features['temperature'] = df[temp_column]
        features['precipitation'] = df[precip_column]

        # Rolling averages
        for window in [7, 14, 30]:
            features[f'temp_roll_{window}'] = df[temp_column].rolling(window=window).mean()
            features[f'precip_roll_{window}'] = df[precip_column].rolling(window=window).mean()

        # Seasonal features
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            features['month'] = df['date'].dt.month
            features['season'] = (df['date'].dt.month % 12 + 3) // 3  # 1=Winter, 2=Spring, etc.
            features['day_of_year'] = df['date'].dt.dayofyear

        # Fill NaN
        features = features.fillna(method='bfill').fillna(method='ffill')

        self.feature_names = features.columns.tolist()

        return features

    def train(self, df, temp_column='temperature', precip_column='precipitation',
              test_size=0.2):
        """
        Train classification model.

        Args:
            df: DataFrame with climate data
            temp_column: Name of temperature column
            precip_column: Name of precipitation column
            test_size: Test set size

        Returns:
            Training metrics
        """
        # Prepare features and labels
        X = self.prepare_features(df, temp_column, precip_column)
        y = self.create_climate_labels(df, temp_column, precip_column)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Train model
        self.model.fit(X_train, y_train)
        self.fitted = True

        # Evaluate
        y_pred = self.model.predict(X_test)

        metrics = {
            'accuracy': float(self.model.score(X_test, y_test)),
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }

        return metrics

    def predict(self, df, temp_column='temperature', precip_column='precipitation'):
        """
        Predict climate patterns.

        Args:
            df: DataFrame with climate data
            temp_column: Name of temperature column
            precip_column: Name of precipitation column

        Returns:
            Array of predictions
        """
        if not self.fitted:
            raise ValueError("Model not trained yet!")

        X = self.prepare_features(df, temp_column, precip_column)
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        return predictions, probabilities

    def get_feature_importance(self):
        """Get feature importance from trained model."""
        if not self.fitted:
            raise ValueError("Model not trained yet!")

        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        return importance_df.to_dict('records')

    def save_model(self, filepath):
        """Save model."""
        joblib.dump(self.model, filepath)

    def load_model(self, filepath):
        """Load model."""
        self.model = joblib.load(filepath)
        self.fitted = True
