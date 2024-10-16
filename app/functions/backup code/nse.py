import os
import requests
import pickle
import random
import pandas as pd
from datetime import datetime, timedelta
from hashlib import sha256

# Define a decorator for caching
def cached(app_name, timeout=10):
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

# List of user agents for rotation
# user_agents = [
#     'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
#     'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
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

# Function to fetch data from NSE with caching
@cached("nse_cache", timeout=3600)  # 1 hour timeout
def fetch_nse_data(url):
    # Rotate User-Agent for each request
    headers = {
        'User-Agent': random.choice(user_agents),
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.nseindia.com/'
    }

    # Initial request to fetch cookies (replace with the actual URL that sets the cookies)
    initial_url = "https://www.nseindia.com/"
    session.get(initial_url, headers=headers)
    
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Response content is not valid JSON")
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

