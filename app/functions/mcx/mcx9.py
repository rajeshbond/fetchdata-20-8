import requests
import json
import random
import time

# List of user agents to rotate
# user_agents = [
#     'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
#     'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
#     'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36',
#     'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
# ]

user_agents = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36'
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

# Function to initialize the session (to maintain cookies and state)
def initialize_session():
    session = requests.Session()
    return session

# Function to fetch data dynamically from any MCX URL using a session
def fetch_data_from_mcx(session, url, payload=None):
    headers = generate_headers()  # Generate dynamic headers
    
    if payload is None:
        payload = "{}"  # Default empty payload for POST requests
    
    try:
        # Make the POST request with the session to handle cookies
        response = session.post(url, headers=headers, data=payload)
        
        # Check for successful response
        if response.status_code == 200:
            try:
                # Decode the JSON response
                json_data = response.json()
                return json.dumps(json_data, indent=4)
            except json.JSONDecodeError:
                return "Failed to decode JSON"
        else:
            return f"Failed with status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# Example function to fetch the data from "GetMarketWatch" URL
def fetch_mcx_market_watch_data():
    # Initialize session
    session = initialize_session()
    
    # URL for fetching the Market Watch data
    # mcx_market_watch_url = "https://www.mcxindia.com/backpage.aspx/GetMarketWatch"
    # mcx_market_watch_url = "https://www.mcxindia.com/backpage.aspx/GetMarketWatch"
    mcx_market_watch_url = "https://www.mcxindia.com/backpage.aspx/GetHeatMap"
    # mcx_market_watch_url = "https://www.mcxindia.com/backpage.aspx/GetGainer"
    # mcx_market_watch_url = "https://www.mcxindia.com/backpage.aspx/GetMCXIComdexIndicesDetails"
    # Optional payload, leave as empty for now
    payload = "{}"
    # payload = {
    #     "Instrument_Identifier": "0",
    #     "Lang": "en"
    # }
    
    # Fetch the data from the Market Watch URL
    result = fetch_data_from_mcx(session, mcx_market_watch_url, payload)
    
    # Print the result
    print(result)

# Run the function to fetch the market watch data
fetch_mcx_market_watch_data()
