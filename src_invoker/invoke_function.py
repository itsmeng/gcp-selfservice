import requests
from google.auth.transport.requests import Request
import google.oauth2.id_token
import parameters
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)


def fetch_token(function_url):
    request = Request()  # Simplified import usage
    try:
        token = google.oauth2.id_token.fetch_id_token(request, function_url)
    except Exception as e:
        raise
    if token is None:
        raise ValueError("Unable to generate token. Check your credentials.")
    return token

def create_headers(token):
    headers = {  # Use a variable for clarity
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    return headers

def send_request(function_url, headers, data):
    response = requests.post(function_url, headers=headers, json=data, timeout=70)  # Use a variable for clarity
    return response

def handle_response(response):
    if response.status_code == 200:
        logging.info("Function called successfully!")
    else:
        logging.info(f"Error calling function. Status code: {response.status_code}")
    logging.info(f"Response: {response.text}")

def call_cloud_function(function_url, data):
    token = fetch_token(function_url)
    headers = create_headers(token)
    response = send_request(function_url, headers, data)
    handle_response(response)
    return response

if __name__ == "__main__":
    # get values from parameters.py
    project_id = parameters.project_id
    region = parameters.region
    function_name = parameters.function_name
    function_url = f"https://{region}-{project_id}.cloudfunctions.net/{function_name}"
    logging.info(f"Target function: {function_url}")  # Capitalized "Target" for consistency
    data = {
        "action": "hello",
        "target": "world",
    }
    call_cloud_function(function_url , data)