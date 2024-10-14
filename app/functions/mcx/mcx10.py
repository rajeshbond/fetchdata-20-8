import requests
import json
import random

# List of user agents to rotate
user_agents = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
]

# Function to generate dynamic headers for each request
def generate_headers():
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US,en;q=0.9",
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
        "Cache-Control": "no-cache"
    }

# Function to initialize the session and get cookies
def initialize_session_and_get_cookies():
    session = requests.Session()
    
    # Make an initial GET request to fetch cookies
    mcx_home_url = "https://www.mcxindia.com"
    
    # GET request to MCX homepage to get session cookies
    session.get(mcx_home_url, headers={"User-Agent": random.choice(user_agents)})
    
    # Return the session with cookies set
    return session

# Function to fetch data dynamically from any MCX URL using a session
def fetch_data_from_mcx(session, url, payload=None):
    headers = generate_headers()  # Generate dynamic headers

    try:
        # Make the POST request with the session (cookies are already set in session)
        response = session.post(url, headers=headers, data=json.dumps(payload))
        
        # Debugging: print request and response status
        # print(f"Request URL: {url}")
        # print(f"Request Headers: {json.dumps(headers, indent=4)}")
        # print(f"Payload Sent: {json.dumps(payload, indent=4)}")
        # print(f"Response Status Code: {response.status_code}")

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

# Function to fetch the data from the MCXIComdexIndicesDetails URL
def fetch_mcx_icomdex_indices_data():
    # Initialize session and get cookies
    session = initialize_session_and_get_cookies()
    
    # URL for fetching the MCXIComdex Indices Details
    mcx_icomdex_indices_url = "https://www.mcxindia.com/backpage.aspx/GetMCXIComdexIndicesDetails"
    # mcx_icomdex_indices_url = "https://www.mcxindia.com/backpage.aspx/GetGainer"
    
    # Payload: Sending the provided payload
    payload = {
        "Instrument_Identifier": "0",
        "Lang": "en"
    }
    # payload = "{}"
    # Fetch the data from the MCXIComdex Indices Details URL
    result = fetch_data_from_mcx(session, mcx_icomdex_indices_url, payload)
    
    # Print the result
    print(result)

# Run the function to fetch the MCXIComdex Indices Details data
if __name__ == "__main__":
    fetch_mcx_icomdex_indices_data()
