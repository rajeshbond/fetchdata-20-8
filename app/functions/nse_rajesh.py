import os
import requests
import pickle
import random
import time
from datetime import datetime, timedelta
from hashlib import sha256
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import signal
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define a decorator for caching
def cached(app_name: str, timeout: int = 15):
    """Caching decorator to cache function results."""
    def _cached(function):
        def wrapper(*args, **kwargs):
            # Create a directory for caching
            home_dir = os.path.expanduser("~")
            cache_dir = os.path.join(home_dir, '.cache', app_name)
            os.makedirs(cache_dir, exist_ok=True)

            # Generate a unique key from the function name and arguments
            key = function.__name__ + str(args) + str(kwargs)
            key_hash = sha256(key.encode()).hexdigest()
            path = os.path.join(cache_dir, f"{key_hash}.pkl")

            now = datetime.now()
            if os.path.isfile(path):
                with open(path, 'rb') as fp:
                    cached_data = pickle.load(fp)
                    if now - cached_data['timestamp'] < timedelta(seconds=timeout):
                        logging.info("Returning cached data.")
                        return cached_data['data']

            # Fetch new data and cache it
            data = function(*args, **kwargs)
            with open(path, 'wb') as fp:
                pickle.dump({'data': data, 'timestamp': now}, fp)
            return data
        return wrapper
    return _cached

# Start a session to persist cookies across requests
session = requests.Session()

# Configure retry logic for the session
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

# List of user agents for rotation
user_agents = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

def get_random_user_agent() -> str:
    """Select a random user agent from the list."""
    return random.choice(user_agents)

# Function to fetch data from NSE with caching
@cached("nse_cache", timeout=15)  # Adjusted timeout to 15 seconds
def fetch_nse_data(url: str):
    """Fetch data from the given URL with caching."""
    headers = {
        'User-Agent': get_random_user_agent(),
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

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
    except ValueError:
        logging.error("Response content is not valid JSON")
    
    return None

# Auto-refresh logic to fetch data every 15 seconds
def auto_refresh_data(url: str):
    """Continuously fetch data from the provided URL every 15 seconds."""
    def signal_handler(sig, frame):
        logging.info("Shutting down the data fetcher...")
        sys.exit(0)

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        data = fetch_nse_data(url)
        if data:
            logging.info(f"Fetched Data: {data}")
        else:
            logging.warning("Failed to fetch data.")
        
        time.sleep(15)  # Wait 15 seconds before the next fetch

# Example usage
if __name__ == "__main__":
    nse_url = "https://www.nseindia.com/api/marketStatus"  # Replace with the actual NSE API endpoint
    auto_refresh_data(nse_url)
