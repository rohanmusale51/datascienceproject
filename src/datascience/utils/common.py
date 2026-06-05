import os
from mlflow import data
from mlflow import data
import yaml
from src.datascience import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError, BoxKeyError
from typing import List

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.

    Args:
        path_to_yaml (Path): The file path to the YAML file.
    Returns:
        ConfigBox: A ConfigBox object containing the contents of the YAML file.
    Raises:
        FileNotFoundError: If the specified YAML file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    if not os.path.exists(path_to_yaml):
        raise FileNotFoundError(f"The specified YAML file does not exist: {path_to_yaml}")
    
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Successfully read YAML file: {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"The YAML file is empty: {path_to_yaml}")
    
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise e


@ensure_annotations
def create_directories(path_to_directories: List[Path]) -> None:
    """
    Creates directories from a list of directory paths.

    Args:
        path_to_directories (List[Path]): A list of directory paths to be created.
    Returns:
        None
    Raises:       OSError: If there is an error creating any of the directories.
    """
    for path in path_to_directories:
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created successfully: {path}")
        except OSError as e:
            logger.error(f"Error creating directory {path}: {e}")
            raise e

@ensure_annotations
def save_json(path: Path, data: dict) -> None:
    """
    Saves a dictionary as a JSON file.

    Args:
        path (Path): The file path where the JSON file will be saved.
        data (dict): The dictionary to be saved as JSON.
    Returns:
        None
    Raises:
        OSError: If there is an error writing to the file.
        TypeError: If the data provided is not serializable to JSON.
    """
    try:
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            logger.info(f"Data successfully saved to JSON file: {path}")
    except OSError as e:
        logger.error(f"Error writing to file {path}: {e}")
        raise e
    except TypeError as e:
        logger.error(f"Data provided is not serializable to JSON: {e}")
        raise e

@ensure_annotations

def load_json(path: Path) -> dict:
    """
    Loads a JSON file and returns its contents as a dictionary.

    Args:
        path (Path): The file path to the JSON file.
    Returns:
        dict: A dictionary containing the contents of the JSON file.
    Raises:
        FileNotFoundError: If the specified JSON file does not exist.
        json.JSONDecodeError: If there is an error parsing the JSON file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified JSON file does not exist: {path}")
    
    try:
        with open(path, 'r') as json_file:
            content = json.load(json_file)
            logger.info(f"Successfully loaded JSON file: {path}")
            return ConfigBox(content)
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file: {e}")
        raise e

@ensure_annotations
def save_bin(data: Any, path: Path) -> None:
    """
    Saves data to a binary file using joblib.

    Args:
        data (Any): The data to be saved.
        path (Path): The file path where the binary file will be saved.
    Returns:
        None
    Raises:
        OSError: If there is an error writing to the file.
        TypeError: If the data provided cannot be serialized by joblib.
    """
    try:
        joblib.dump(data, path)
        logger.info(f"Data successfully saved to binary file: {path}")
    except OSError as e:
        logger.error(f"Error writing to file {path}: {e}")
        raise e
    except TypeError as e:
        logger.error(f"Data provided cannot be serialized by joblib: {e}")
        raise e
    
@ensure_annotations
def load_bin(path: Path) -> ConfigBox:
    """
    Loads data from a binary file using joblib.

    Args:
        path (Path): The file path to the binary file.
    Returns:
        Any: The data loaded from the binary file.
    Raises:
        FileNotFoundError: If the specified binary file does not exist.
        TypeError: If the data provided cannot be deserialized by joblib.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified binary file does not exist: {path}")

    try:
        data = joblib.load(path)
        logger.info(f"Data successfully loaded from binary file: {path}")
        return data
    except TypeError as e:
        logger.error(f"Data provided cannot be deserialized by joblib: {e}")
        raise e
    
 