import os
import requests
import pickle
import random
from datetime import datetime, timedelta
from hashlib import sha256

# Define a decorator for caching
def cached(app_name, timeout=3600):
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
user_agents = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

# Function to fetch data from MCX with caching
@cached("mcx_cache", timeout=3600)  # 1 hour timeout
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

    # Initial request to fetch cookies (MCX main page)
    initial_url = "https://www.mcxindia.com/"
    session.get(initial_url, headers=headers)

    # Fetching the actual data from MCX
    response = session.post(url, headers=headers, data="{}")
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Response content is not valid JSON")
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Example usage
mcx_url = "https://www.mcxindia.com/BackPage.aspx/GetTicker"
mcx_data = fetch_mcx_data(mcx_url)

# Print the fetched data (cached if already retrieved within the timeout period)
print(mcx_data)
