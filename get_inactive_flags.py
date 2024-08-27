import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv(override=True)

# Fetch environment variables
api_token = os.getenv("LD_API_TOKEN")
project_key = os.getenv("LD_PROJECT_KEY")
environment_key = os.getenv("LD_ENVIRONMENT_KEY")

# Check if variables are set
if not api_token or not project_key or not environment_key:
    raise ValueError("One or more environment variables are not set.")

print(f"Using project: {project_key}")
print(f"Using environment: {environment_key}")

# API request to get flag statuses
url = f"https://app.launchdarkly.com/api/v2/flag-statuses/{project_key}/{environment_key}"
headers = {
    "Authorization": f"{api_token}",
    
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
response_json = response.json()

# Handle invalid token or other errors
if response.status_code == 401:
    print("Error: Invalid API token. Please check your token and try again.")
elif response.status_code != 200:
    print(f"Error: Received status code {response.status_code}. Response: {response_json}")
else:
    # Process the 'items' key from the response
    try:
        flag_statuses = response_json['items']
        # Filter and collect URLs of inactive flags
        inactive_flags = [
            flag['_links']['parent']['href'] for flag in flag_statuses if flag['name'] == 'inactive'
        ]

        # Output the inactive flags in JSON format
        output = {"inactive_flags": inactive_flags}
        print(json.dumps(output, indent=2))

    except KeyError as e:
        print(f"KeyError: {e} not found in the response. Please check the response structure.")
