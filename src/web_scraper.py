import re
import os
import requests
from bs4 import BeautifulSoup
import hashlib
import configparser


def fetch_text(url):
    """
    Fetches the text content of a webpage.
    Args:
        url (str): The URL of the webpage to fetch.
    Returns:
        str: The text content of the webpage, or an error message if the webpage couldn't be fetched.
    """
    response = requests.get(url)
    if response.status_code != 200:
        return "Error fetching webpage."
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()


def sanitize_filename(url):
    """
    Sanitizes the given URL to create a valid and shorter filename by hashing the URL.
    Args:
        url (str): The URL to sanitize.
    Returns:
        str: The sanitized filename.
    """
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return url_hash


def get_output_folder():
    """
    Returns the output folder path from the config file.
    Returns:
        str: The output folder path.
    """
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    create_folder_if_not_exists(config["path_settings"]["results_folder"])
    return config["path_settings"]["results_folder"]


def create_folder_if_not_exists(folder):
    """
    Creates the specified folder if it doesn't already exist.
    Args:
        folder (str): The folder path to create.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
