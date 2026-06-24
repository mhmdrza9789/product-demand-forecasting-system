import os
import sys
import json
import yaml
import joblib

from pathlib import Path
from typing import Any

# from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError

from src.productdemand.exception.custom_exception import CustomException
from src.productdemand.logger.custom_logger import get_logger


logger = get_logger(__name__)


# @ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty.
        CustomException: If any other error occurs.

    Returns:
        ConfigBox: YAML content as ConfigBox.
    """
    try:
        with open(path_to_yaml, "r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)

            if content is None:
                raise ValueError("YAML file is empty")

            logger.info("YAML file loaded successfully", path=str(path_to_yaml))
            return ConfigBox(content)

    except BoxValueError:
        raise ValueError("YAML file is empty")

    except Exception as e:
        raise CustomException(e, sys)


# @ensure_annotations
def create_directories(path_to_directories: list[Path], verbose: bool = True) -> None:
    """
    Creates a list of directories.

    Args:
        path_to_directories (list[Path]): List of directory paths to create.
        verbose (bool, optional): Whether to log directory creation. Defaults to True.

    Raises:
        CustomException: If directory creation fails.
    """
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logger.info("Created directory", path=str(path))

    except Exception as e:
        raise CustomException(e, sys)


# @ensure_annotations
def save_json(path: Path, data: dict) -> None:
    """
    Saves data to a JSON file.

    Args:
        path (Path): Path to JSON file.
        data (dict): Data to save.

    Raises:
        CustomException: If saving fails.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        logger.info("JSON file saved successfully", path=str(path))

    except Exception as e:
        raise CustomException(e, sys)


# @ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads data from a JSON file.

    Args:
        path (Path): Path to JSON file.

    Raises:
        CustomException: If loading fails.

    Returns:
        ConfigBox: JSON content as ConfigBox.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)

        logger.info("JSON file loaded successfully", path=str(path))
        return ConfigBox(content)

    except Exception as e:
        raise CustomException(e, sys)


# @ensure_annotations
def save_bin(data: Any, path: Path) -> None:
    """
    Saves an object as a binary file using joblib.

    Args:
        data (Any): Object to save.
        path (Path): Path to binary file.

    Raises:
        CustomException: If saving fails.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(value=data, filename=path)

        logger.info("Binary file saved successfully", path=str(path))

    except Exception as e:
        raise CustomException(e, sys)


# @ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads an object from a binary file using joblib.

    Args:
        path (Path): Path to binary file.

    Raises:
        CustomException: If loading fails.

    Returns:
        Any: Loaded object.
    """
    try:
        data = joblib.load(path)

        logger.info("Binary file loaded successfully", path=str(path))
        return data

    except Exception as e:
        raise CustomException(e, sys)
