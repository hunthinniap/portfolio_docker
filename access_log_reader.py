import re
import json
import requests
import os

# Mock function for IP to location translation
def ip_to_location(ip_address):
    # In a real scenario, replace this with a call to an IP geolocation API or library
    # This is a placeholder for demonstration purposes
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    if response.status_code == 200:
        data = response.json()
        location = {
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "org": data.get("org"),
            "postal": data.get("postal"),
        }
        return location
    else:
        return {}

def read_json_file(file_path):
    """Reads the JSON file and returns the data."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_json_file(file_path, data):
    """Writes the data to the JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def remove_duplicates(existing_logs, new_logs):
    """Removes duplicates from the new_logs list."""
    existing_set = {json.dumps(log, sort_keys=True) for log in existing_logs}
    new_unique_logs = [log for log in new_logs if json.dumps(log, sort_keys=True) not in existing_set]
    return new_unique_logs

def add_logs_to_json_file(file_path, new_logs):
    """Reads existing logs, adds new logs if they are not duplicates, and writes them back to the JSON file."""
    existing_logs = read_json_file(file_path)
    unique_logs = remove_duplicates(existing_logs, new_logs)
    updated_logs = existing_logs + unique_logs
    write_json_file(file_path, updated_logs)


log_pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" "\d+\.\d+\.\d+\.\d+" response-time=(\d+\.\d+)'


parsed_logs = []

log_directory = 'var/logs/hunthinniap.pythonanywhere.com.access.log'




with open(log_directory, 'r') as file:
    lines = file.readlines()

for line in lines:
    match = re.match(log_pattern, line)
    if match:
        request_details = match.group(3)
        
        # Filter out specific request types or paths
        if 'POST' in request_details or '/static/styles.css' in request_details or '/favicon.ico' in request_details:
            continue  # Skip this log entry

        ip_address = match.group(1)
        location = ip_to_location(ip_address)  # Translate IP address to location

        data = {
            'ip_address': ip_address,
            'location': location,  # Add location data
            'timestamp': match.group(2),
            'request': request_details,
            'response_code': match.group(4),
            'response_size': match.group(5),
            'referrer': match.group(6),
            'user_agent': match.group(7),
            'response_time': match.group(8)
        }
        parsed_logs.append(data)

# Save to JSON file
add_logs_to_json_file('access_logs.json', parsed_logs)