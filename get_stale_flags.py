import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta, timezone
import time

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

# Base URL for LaunchDarkly API
base_url = "https://app.launchdarkly.com"

# Define headers once to be reused
headers = {
    "Authorization": f"{api_token}",
    "Content-Type": "application/json"
}

# Function to fetch all feature flags with pagination and rate limiting handling
def fetch_all_flags(project_key, api_token):
    flags = []
    url = f"{base_url}/api/v2/flags/{project_key}?limit=20"
    
    while url:
        response = requests.get(url, headers=headers)
        
        # Check if rate limit was exceeded
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            continue

        data = response.json()
        flags.extend(data['items'])
        next_link = data['_links'].get('next', {}).get('href')
        if next_link:
            url = f"{base_url}{next_link}"
        else:
            url = None

        # Optional: Delay between requests to avoid hitting rate limits
        time.sleep(1)
    
    return flags

# Fetch all flags using pagination
all_flags = fetch_all_flags(project_key, api_token)

# API request to get flag statuses with rate limiting handling
def get_flag_statuses(url):
    while True:
        response = requests.get(url, headers=headers)
        
        # Check if rate limit was exceeded
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            continue

        return response.json()['items']

statuses_url = f"https://app.launchdarkly.com/api/v2/flag-statuses/{project_key}/{environment_key}"
flag_statuses = get_flag_statuses(statuses_url)

# Define the date threshold for flags older than 30 days (use timezone-aware datetime)
date_threshold = datetime.now(timezone.utc) - timedelta(days=30)

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
        status = status_info['name'] if status_info else 'unknown'
        
        # Determine the relevant date to check (lastRequested or creationDate)
        last_requested_str = status_info.get('lastRequested') if status_info else None
        
        if last_requested_str:
            try:
                # Try parsing with milliseconds
                last_requested = datetime.strptime(last_requested_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                # Fall back to parsing without milliseconds
                last_requested = datetime.strptime(last_requested_str, '%Y-%m-%dT%H:%M:%S%z')
            last_requested = last_requested.replace(tzinfo=timezone.utc)  # Make it timezone-aware
        else:
            creation_date = datetime.fromtimestamp(flag['creationDate'] / 1000, tz=timezone.utc)
            last_requested = creation_date
        
        # Apply filtering logic
        if is_temporary and (status in ['inactive', 'launched', 'unknown']) and last_requested < date_threshold:
            stale_flags.append({
                "key": flag_key,
                "name": flag['name'],
                "status": status,
                "lastRequested": last_requested_str or "Never evaluated (using creation date)",
                "temporary": is_temporary
            })

# Output the stale flags in JSON format
output = {"stale_flags": stale_flags}
print(json.dumps(output, indent=2))

# Print the total count of stale flags
print(f"Total stale flags: {len(stale_flags)}")
