import requests
import json
import random
import time

# Define the URL
url = "https://www.mcxindia.com/BackPage.aspx/GetTicker"
# url = "https://www.mcxindia.com"

# List of user agents to rotate
user_agents = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
]

# List of Accept-Language headers to rotate
accept_language_options = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "en-IN,en;q=0.8",
    "fr-FR,fr;q=0.7,en;q=0.6"
]

# List of Cache-Control options to rotate
cache_control_options = [
    "no-cache",
    "no-store",
    "max-age=0",
    "must-revalidate"
]

# Function to generate dynamic headers for each request
def generate_headers():
    return {
        "Accept": "*/*",
        "Accept-Encoding": random.choice(["gzip", "deflate", "br", "zstd"]),
        "Accept-Language": random.choice(accept_language_options),
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Cookie": "ASP.NET_SessionId=tf5lsipa5hau4tms0pr2druw; _gid=GA1.2.1622783788.1727249918;",
        "Host": "www.mcxindia.com",
        "Origin": "https://www.mcxindia.com",
        "Referer": "https://www.mcxindia.com/",
        "Sec-CH-UA-Mobile": "?1",
        "Sec-CH-UA-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": random.choice(user_agents),
        "X-Requested-With": "XMLHttpRequest",
        "Cache-Control": random.choice(cache_control_options)  # Rotating Cache-Control
    }

# The data sent with the POST request (empty payload)
data = "{}"

# Function to send the POST request
def fetch_data():
    headers = generate_headers()  # Generate dynamic headers
    
    # Make the POST request
    response = requests.post(url, headers=headers, data=data)
    
    # Check for successful response
    if response.status_code == 200:
        try:
            # Directly decode the JSON response
            json_data = response.json()
            return json.dumps(json_data, indent=4)
        except json.JSONDecodeError:
            return "Failed to decode JSON"
    else:
        return f"Failed with status code: {response.status_code}"

# Introduce random delays between requests to avoid detection
time.sleep(random.uniform(1, 3))

# Fetch the data and print the output
result = fetch_data()
print(result)
