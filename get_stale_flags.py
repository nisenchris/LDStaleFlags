import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
api_token = os.getenv("LD_API_TOKEN")
project_key = os.getenv("LD_PROJECT_KEY")
environment_key = os.getenv("LD_ENVIRONMENT_KEY")

# Check if variables are set
if not api_token or not project_key or not environment_key:
    raise ValueError("One or more environment variables are not set.")

# API request to get all feature flags
flags_url = f"https://app.launchdarkly.com/api/v2/flags/{project_key}"
headers = {
    "Authorization": f"{api_token}",
    "Content-Type": "application/json"
}

flags_response = requests.get(flags_url, headers=headers)
all_flags = flags_response.json()['items']

# API request to get flag statuses
statuses_url = f"https://app.launchdarkly.com/api/v2/flag-statuses/{project_key}/{environment_key}"
statuses_response = requests.get(statuses_url, headers=headers)
flag_statuses = statuses_response.json()['items']

# Define the date threshold for flags older than 30 days
date_threshold = datetime.utcnow() - timedelta(days=30)

# Create a dictionary to map flag keys to their statuses
status_map = {status['_links']['parent']['href'].split('/')[-1]: status for status in flag_statuses}

# Filter and combine the data
stale_flags = []
for flag in all_flags:
    flag_key = flag['key']
    status_info = status_map.get(flag_key)

    if status_info:
        # Check if the flag is temporary
        is_temporary = flag.get('temporary', False)
        # Get the status (inactive or launched)
        status = status_info['name']
        # Check the lastRequested date
        last_requested = datetime.strptime(status_info['lastRequested'], '%Y-%m-%dT%H:%M:%SZ')

        # Apply filtering logic
        if is_temporary and (status in ['inactive', 'launched']) and last_requested < date_threshold:
            stale_flags.append({
                "key": flag_key,
                "name": flag['name'],
                "status": status,
                "lastRequested": status_info['lastRequested'],
                "temporary": is_temporary
            })

# Output the stale flags in JSON format
output = {"stale_flags": stale_flags}
print(json.dumps(output, indent=2))
