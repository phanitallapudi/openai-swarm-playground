from datetime import datetime
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os
import base64
import requests
import string
import random

from app.middleware.logging_middleware import logger

load_dotenv()

def get_current_datetime():
    logger.info("using get_current_datetime tool")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Agent Functions
def get_weather(location, time="now"):
    """
    Fetch live weather data for a given location.
    """
    logger.info("using get_weather tool")
    API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    BASE_URL = "https://api.openweathermap.org/data/2.5/"

    if time == "now":
        endpoint = f"{BASE_URL}weather"
    else:
        return {"error": "Only 'now' is supported for time parameter."}

    params = {"q": location, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except KeyError:
        return {"error": "Unexpected response format. Please check the API or your query."}


def send_email(recipient, subject, body, attachments=None):
    """
    Send an email using SendGrid.
    """
    logger.info("using send_email tool")
    message = Mail(
        from_email=os.getenv("MAIL_USERNAME"),
        to_emails=recipient,
        subject=subject,
        html_content=body,
    )

    if attachments:
        for attachment in attachments:
            with open(attachment["file_path"], "rb") as f:
                data = f.read()
                encoded_file = base64.b64encode(data).decode()

            message.attachment = {
                "content": encoded_file,
                "type": attachment["file_type"],
                "filename": attachment["file_name"],
            }

    try:
        sg = SendGridAPIClient(os.getenv("MAIL_API_KEY"))
        response = sg.send(message)
        if response.status_code == 202:
            return "Email sent successfully."
        else:
            return {"error": f"Failed to send email. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
    
def search_duckduckgo(query):
    logger.info("using search_duckduckgo tool")
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json"}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()
    
    return results

def generate_random_string(length=8):
    logger.info("using generate_random_string tool")
    
    # Ensure length is an integer
    length = int(length)
    
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def factorial(n):
    logger.info("using factorial tool")
    n = int(n)
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def reverse_string(s):
    logger.info("using reverse_string tool")
    return s[::-1]

def longest_word(sentence):
    logger.info("using longest_word tool")
    words = sentence.split()
    return max(words, key=len)

def is_palindrome(word):
    logger.info("using is_palindrome tool")
    return word == word[::-1]

def fibonacci_series(n):
    logger.info("using fibonacci_series tool")
    n = int(n)
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def generate_random_color():
    logger.info("using generate_random_color tool")
    return f"#{random.randint(0, 0xFFFFFF):06x}"

def count_words(text):
    logger.info("using count_words tool")
    count = 0
    for _ in range(len(text)):
        count += 1
    return count

def read_txt_file(file_path):
    """
    Reads the content of a .txt file and returns it as a string.
    
    Parameters:
        file_path (str): The path to the .txt file.
        
    Returns:
        str: The content of the file.
    """
    logger.info("using read_txt_file tool")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at '{file_path}' was not found."
    except IOError as e:
        return f"Error: An IOError occurred. Details: {e}"
    
import socket

def get_ip_address():
    """Returns the IP address of the machine."""
    logger.info("using get_ip_address tool")
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)
