import json
import logging
import os
from typing import Dict


def _load_root_dir() -> str:
    """
    Finds the location of the project root.
    :return: Root location of the project.
    """
    location = os.path.abspath(os.path.dirname(__file__))
    root_folder = "credentials"
    while not os.path.isdir(os.path.join(location, root_folder)):
        location = os.path.dirname(location)
    return os.path.join(location, root_folder)


def _read_credentials(filename: str) -> Dict[str, str]:
    """
    Helper to load the secret classes
    """
    try:
        with open(_load_root_dir() + "/" + filename, encoding="utf-8") as f:
            config: Dict[str, str] = json.load(f)
        return config
    except FileNotFoundError:
        logging.error(
            f"File '{filename}' not available! See the README where to get the secret from."
        )
    return {}


def read_openai_credentials() -> str:
    """
    This will read the internal config file and return the corresponding API_KEY stored in it.
    :return: api_key: api key for OpenAI
    """
    filename = "credentials.json"
    config = _read_credentials(filename)
    return config["OPENAI_API_KEY"]


def read_newsapi_credentials() -> str:
    """
    This will read the internal config file and return the corresponding API_KEY stored in it.
    :return: api_key: api key for Newsapi
    """
    filename = "credentials.json"
    config = _read_credentials(filename)
    return config["NEWSAPI_API_KEY"]


def read_serpapi_credentials() -> str:
    """
    This will read the internal config file and return the corresponding API_KEY stored in it.
    :return: api_key: api key for Serpapi
    """
    filename = "credentials.json"
    config = _read_credentials(filename)
    return config["SERPAPI_API_KEY"]

def read_pinecone_credentials() -> str:
    """
    This will read the internal config file and return the corresponding API_KEY stored in it.
    :return: api key: api key for Pinecone
    """
    filename = "credentials.json"
    config = _read_credentials(filename)
    return config["PINECONE_API_KEY"]


def read_huggingface_hub_credentials() -> str:
    """
    This will read the internal config file and return the corresponding API_KEY stored in it.
    :return: api key: api key for Huggingface Hub
    """
    filename = "credentials.json"
    config = _read_credentials(filename)
    return config["HUGGINGFACEHUB_API_TOKEN"]
