import os
import requests
import random
import time

# Start a session to persist cookies across requests
session = requests.Session()

# List of user agents for rotation
user_agents = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

# Function to add random delays between requests to avoid detection
def random_delay(min_delay=1, max_delay=5):
    delay = random.uniform(min_delay, max_delay)
    print(f"Sleeping for {delay:.2f} seconds to avoid detection...")
    time.sleep(delay)

# Function to fetch data from MCX without caching
def fetch_mcx_data(url):
    # Rotate User-Agent for each request
    headers = {
        'User-Agent': random.choice(user_agents),
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.mcxindia.com/',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # Introduce a random delay between requests to avoid hitting the server too quickly
    random_delay(min_delay=2, max_delay=6)

    # Initial request to fetch cookies (MCX main page)
    initial_url = "https://www.mcxindia.com/"
    session.get(initial_url, headers=headers)

    # Fetching the actual data from MCX
    response = session.post(url, headers=headers, data="{}")

    # Debugging - Print Status Code and Response Headers
    # print(f"Status Code: {response.status_code}")
    # print(f"Response Headers: {response.headers}")

    if response.status_code == 200:
        try:
            # Debugging - Print Raw Response Text
            # print(f"Raw Response Text: {response.text}")
            return response.json()  # Attempt to parse JSON response
        except ValueError:
            print("Response content is not valid JSON. Printing raw response content for debugging.")
            # print(response.text)
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Example usage
mcx_url = "https://www.mcxindia.com/BackPage.aspx/GetTicker"
mcx_data = fetch_mcx_data(mcx_url)

# Print the fetched data
if mcx_data:
    print("Fetched MCX Data:")
    print(mcx_data)
else:
    print("No data fetched.")
