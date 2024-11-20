import os
import requests
import json
import logging
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration variables
api_management_gateway_url = os.getenv("API_MANAGEMENT_GATEWAY_URL")
model = os.getenv("DEPLOYMENT_NAME")
subscription_key = os.getenv("APIM_SUBSCRIPTION_KEY")
api_version = os.getenv("API_VERSION", "2024-03-01-preview") # Update to your API_Version for AOAI

# Validate environment variables
if not api_management_gateway_url:
    raise ValueError("Missing API_MANAGEMENT_GATEWAY_URL environment variable.")
if not model:
    raise ValueError("Missing DEPLOYMENT_NAME environment variable.")
if not subscription_key:
    raise ValueError("Missing APIM_SUBSCRIPTION_KEY environment variable.")

# Construct the API endpoint
completions_endpoint = f"{api_management_gateway_url}/openai/deployments/{model}/chat/completions?api-version={api_version}"

# Define headers
request_headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "application/json",
    # Add traceability headers for observability
    "Request-ID": str(datetime.utcnow().timestamp()),  # Unique ID for this request
    "Client-Name": "AzureOpenAITrainingDemo",  # Example client identifier
}

# Function to make a chat completion request
def make_chat_completion_request(endpoint, headers, body):
    """Send a POST request to the Azure OpenAI API via APIM."""
    try:
        response = requests.post(endpoint, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

# Function to log metrics and observability data
def log_observability(data, status_code):
    """Simulates logging observability metrics."""
    logging.info("Simulating Observability Metrics:")
    logging.info(f"Status Code: {status_code}")
    logging.info(f"Request ID: {request_headers['Request-ID']}")
    logging.info(f"Timestamp: {datetime.utcnow().isoformat()}")
    if status_code == 200:
        logging.info(f"Response Usage: {json.dumps(data.get('usage', {}), indent=2)}")

# Dynamic user input
user_message = input("Enter your question: ")

# Request body
request_body = {
    "messages": [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": user_message}
    ],
    "max_tokens": 200,
    "temperature": 0.7,
    "top_p": 0.95,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

# Log the request
logging.info(f"Posting request to {completions_endpoint}")
logging.info(f"Request Headers: {json.dumps(request_headers, indent=2)}")
logging.info(f"Request Body: {json.dumps(request_body, indent=2)}")

# Make the API call
response_data = make_chat_completion_request(completions_endpoint, request_headers, request_body)

# Log the response and observability metrics
if response_data:
    logging.info("Response received:")
    logging.info(json.dumps(response_data, indent=2))
    log_observability(response_data, 200)
else:
    logging.error("Failed to receive a valid response.")
    log_observability({}, 500)
