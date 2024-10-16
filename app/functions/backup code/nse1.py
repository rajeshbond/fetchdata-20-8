import os
import requests
import pickle
import random
import time
from datetime import datetime, timedelta
from hashlib import sha256
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Define a decorator for caching
def cached(app_name, timeout=15):  # 15 seconds timeout
    def _cached(function):
        def wrapper(*args, **kw):
            # Create a directory for caching
            home_dir = os.path.expanduser("~")
            cache_dir = os.path.join(home_dir, '.cache', app_name)
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)

            # Generate a unique key from the function name and arguments
            key = function.__name__ + str(args) + str(kw)
            key_hash = sha256(key.encode()).hexdigest()
            path = os.path.join(cache_dir, key_hash + ".pkl")

            now = datetime.now()
            if os.path.isfile(path):
                with open(path, 'rb') as fp:
                    cached_data = pickle.load(fp)
                    if now - cached_data['timestamp'] < timedelta(seconds=timeout):
                        return cached_data['data']

            # Fetch new data and cache it
            data = function(*args, **kw)
            with open(path, 'wb') as fp:
                pickle.dump({'data': data, 'timestamp': now}, fp)
            return data
        return wrapper
    return _cached

# Start a session to persist cookies across requests
session = requests.Session()

# Configure retry logic for session
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

# List of user agents for rotation
user_agents = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

# Function to fetch data from NSE with caching
@cached("nse_cache", timeout=15)  # Adjusted timeout to 15 seconds
def fetch_nse_data(url):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.nseindia.com/'
    }

    try:
        # Initial request to fetch cookies
        session.get("https://www.nseindia.com/", headers=headers, timeout=10)

        # Fetch the desired data
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        try:
            return response.json()
        except ValueError:
            print("Response content is not valid JSON")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Auto-refresh logic to fetch data every 15 seconds
def auto_refresh_data(url):
    while True:
        data = fetch_nse_data(url)
        if data:
            print(f"Fetched Data at {datetime.now()}: {data}")
        else:
            print(f"Failed to fetch data at {datetime.now()}")
        
        time.sleep(15)  # Wait 15 seconds before the next fetch

# Example usage
if __name__ == "__main__":
    nse_url = "https://www.nseindia.com/api/marketStatus"  # Replace with the actual NSE API endpoint
    auto_refresh_data(nse_url)
