import os
import requests
import json
import logging
from dotenv import load_dotenv
from datetime import datetime
import time
import uuid

# Load environment variables
load_dotenv()

# Configure logging with a cleaner format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Configuration variables
api_management_gateway_url = os.getenv("API_MANAGEMENT_GATEWAY_URL")
model = os.getenv("DEPLOYMENT_NAME")
subscription_key = os.getenv("APIM_SUBSCRIPTION_KEY")
api_version = os.getenv("API_VERSION", "2024-03-01-preview")  # Update to your API version for AOAI

# Validate environment variables
if not api_management_gateway_url:
    raise ValueError("Missing API_MANAGEMENT_GATEWAY_URL environment variable.")
if not model:
    raise ValueError("Missing DEPLOYMENT_NAME environment variable.")
if not subscription_key:
    raise ValueError("Missing APIM_SUBSCRIPTION_KEY environment variable.")

# Construct the API endpoint
completions_endpoint = f"{api_management_gateway_url}/openai/deployments/{model}/chat/completions?api-version={api_version}"

def make_chat_completion_request(endpoint, headers, body):
    """Send a POST request to the Azure OpenAI API via APIM with concise logging."""
    try:
        # Send the request
        response = requests.post(endpoint, headers=headers, json=body)

        # Extract APIM-specific headers
        backend_id = response.headers.get("x-backend-id", "unknown")

        # Log key response details
        logging.info(f"Received response | Status Code: {response.status_code} | Backend: {backend_id}")

        # Check for rate limiting
        if response.status_code == 429:
            logging.warning("Rate limit exceeded (429 Too Many Requests).")

        # Raise exception for HTTP errors
        response.raise_for_status()

        # Return the response data and backend ID
        return response.json(), backend_id
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return None, backend_id
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return None, "unknown"

def simulate_requests(num_requests):
    """Simulate multiple requests to demonstrate APIM interactions."""
    for i in range(num_requests):
        logging.info(f"\nSending Request #{i + 1}")

        # Generate a unique Request-ID for tracing
        request_id = str(uuid.uuid4())

        # Define headers with the unique Request-ID
        request_headers = {
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "application/json",
            "Request-ID": request_id,
            "Client-Name": "AzureOpenAITrainingDemo",
        }

        # Request body with a dynamic user message
        request_body = {
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": f"This is request number {i + 1}. Describe the impact of AI on industry."}
            ],
            "max_tokens": 100,
            "temperature": 0.7,
        }

        # Log key request details
        logging.info(f"Request ID: {request_id}")

        # Make the API call
        response_data, backend_id = make_chat_completion_request(
            completions_endpoint, request_headers, request_body
        )

        # Log summary of the response
        if response_data:
            assistant_reply = response_data["choices"][0]["message"]["content"].strip()
            logging.info(f"Assistant Response: {assistant_reply[:100]}...")  # Log first 100 chars
        else:
            logging.error("Failed to receive a valid response.")

        # Optional: Delay to simulate user behavior
        time.sleep(0.5)  # Adjust as needed

if __name__ == "__main__":
    # Simulate multiple requests to demonstrate APIM interactions
    simulate_requests(num_requests=40)  # Adjust the number of requests as needed
