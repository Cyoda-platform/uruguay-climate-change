#!/usr/bin/env python3
"""
Training pipeline for Uruguay Climate Change models.

This script runs the complete training pipeline:
1. Load and preprocess data
2. Build features
3. Train model
4. Evaluate performance
5. Save model and metrics
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.data.load_data import load_raw_data
from src.data.preprocess import preprocess_pipeline
from src.features.build_features import build_features
from src.models.train_model import split_data, train_model, evaluate_model, save_model
from src.utils.helpers import load_config, setup_logging, save_json
from sklearn.ensemble import RandomForestRegressor


def main(config_path: str):
    """
    Run the training pipeline.

    Args:
        config_path: Path to configuration file
    """
    # Load configuration
    config = load_config(config_path)

    # Setup logging
    setup_logging(config['logging']['log_file'], level=config['logging']['level'])

    print("Starting training pipeline...")

    # 1. Load data
    print("Loading data...")
    # Modify this to load your actual data file
    # df = load_raw_data(f"{config['data']['raw_dir']}/your_data_file.csv")

    # 2. Preprocess data
    print("Preprocessing data...")
    # df = preprocess_pipeline(df)

    # 3. Build features
    print("Building features...")
    # df = build_features(df)

    # 4. Split data
    print("Splitting data...")
    # X_train, X_test, y_train, y_test = split_data(
    #     df,
    #     config['features']['target_column'],
    #     config['model']['test_size'],
    #     config['model']['random_state']
    # )

    # 5. Train model
    print("Training model...")
    # model = RandomForestRegressor(
    #     n_estimators=config['training']['n_estimators'],
    #     max_depth=config['training']['max_depth'],
    #     random_state=config['model']['random_state']
    # )
    # model = train_model(X_train, y_train, model)

    # 6. Evaluate model
    print("Evaluating model...")
    # metrics = evaluate_model(model, X_test, y_test)
    # print(f"Model Performance: {metrics}")

    # 7. Save model and metrics
    print("Saving model...")
    # save_model(model, "models/climate_model.pkl")
    # save_json(metrics, "reports/metrics/training_metrics.json")

    print("Training pipeline complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train climate change prediction model")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/config.yaml",
        help="Path to configuration file"
    )

    args = parser.parse_args()
    main(args.config)
