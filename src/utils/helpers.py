"""Helper functions and utilities."""

import json
import yaml
from pathlib import Path
import logging


def setup_logging(log_file: str = None, level=logging.INFO):
    """
    Setup logging configuration.

    Args:
        log_file: Optional path to log file
        level: Logging level
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=level, format=log_format)


def load_config(config_path: str):
    """
    Load configuration from YAML or JSON file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    path = Path(config_path)

    with open(path, 'r') as f:
        if path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif path.suffix == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")


def save_json(data: dict, file_path: str):
    """
    Save dictionary to JSON file.

    Args:
        data: Dictionary to save
        file_path: Path to save the file
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def ensure_dir(directory: str):
    """
    Ensure directory exists, create if it doesn't.

    Args:
        directory: Path to directory
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
