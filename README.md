# **Python client to demo APIM and OpenAI**

This project demonstrates how to integrate **Azure API Management (APIM)** with **Azure OpenAI** using a Python client.

## **Features**
- Demonstrates how APIM secures and manages access to Azure OpenAI.
- Simulates scenarios like rate limiting, caching, and access control using APIM policies.
- Provides observability metrics for monitoring API usage and performance.

## **Prerequisites**

Before running this demo, ensure the following prerequisites are met:

### **Azure Resources**
1. **Azure API Management (APIM)**:
   - APIM should be configured as a gateway to your Azure OpenAI endpoint.
   - Include policies for features like:
     - Subscription key validation.
     - Rate limiting or throttling.
     - Request and response transformations.
   - Example APIM configuration:
     - Backend: Your Azure OpenAI endpoint URL (e.g., `https://<your-resource-name>.openai.azure.com`).
     - Frontend: Custom API exposed via APIM.

2. **Azure OpenAI**:
   - An Azure OpenAI instance with at least one deployment (e.g., `gpt-4` or `gpt-3.5-turbo`).
   - Your Azure OpenAI service must be reachable by APIM.

### **Local Environment**
- **Python 3.8 or higher**.
- An `.env` file with the following variables:
  ```plaintext
  API_MANAGEMENT_GATEWAY_URL=<Your APIM Gateway URL>
  DEPLOYMENT_NAME=<Your Azure OpenAI Deployment Name>
  APIM_SUBSCRIPTION_KEY=<Your APIM Subscription Key>
  API_VERSION=2024-03-01-preview
  ```

## **Setup Instructions**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/azure-apim-openai-demo.git
   cd azure-apim-openai-demo
   ```

2. **Install Dependencies**
   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   - Create a `.env` file in the root directory based on `.env.example`.
   - Populate it with your Azure resource details (see prerequisites).

4. **Run the Demo**
   - Start the Python script:
     ```bash
     python src/main.py
     ```
   - Follow the prompts to simulate various API scenarios.
