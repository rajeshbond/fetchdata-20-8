import os
import requests
import pickle
import random
import pandas as pd
from datetime import datetime, timedelta
from hashlib import sha256
from bs4 import BeautifulSoup

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

# List of user agents for rotation
user_agents = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
]

# Apply caching to fetch_fii_dii_data with a 1-hour timeout
@cached("fii_dii_cache", timeout=3600)  # 1 hour timeout
def fetch_fii_dii_data():
    url = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"

    # Rotate User-Agent for each request
    headers = {
        "User-Agent": random.choice(user_agents),  # Random User-Agent from the list
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        'Referer': 'https://www.moneycontrol.com/'
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('div', {'class': 'fifi_tblbrd'})

    # Extract table data
    data = []
    if table:
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                data.append({
                    'Date': cols[0].text.strip(),
                    'FII Buy Value': cols[1].text.strip(),
                    'FII Sell Value': cols[2].text.strip(),
                    'FII Net Value': cols[3].text.strip(),
                    'DII Buy Value': cols[4].text.strip(),
                    'DII Sell Value': cols[5].text.strip(),
                    'DII Net Value': cols[6].text.strip()
                })
    print(data)

    return data

def data_cleaning(data):
    df = pd.DataFrame(data)
    
    # Clean 'Date' column: strip and remove newline characters
    df['Date'] = df['Date'].str.strip().replace('\n', '', regex=True)

    # Define the criteria to exclude rows where 'Date' is 'Month till date' or '24-Jul-2024'
    criteria = (df['Date'] != 'Month till date') & (df['Date'] != '24-Jul-2024')

    # Apply the criteria to filter the DataFrame
    filtered_df = df[criteria].copy()  # Ensure we work on a copy to avoid SettingWithCopyWarning

    # Use regex to extract the relevant date
    filtered_df['Date'] = filtered_df['Date'].str.extract(r'(\d{2}-\w{3}-\d{4})')

    # Convert 'Date' column to datetime format
    try:
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d-%b-%Y', errors='coerce')
    except Exception as e:
        print(f"Date conversion error: {e}")
        return []

    # Drop rows where conversion failed (resulting in NaT)
    filtered_df = filtered_df.dropna(subset=['Date'])

    # Filter out weekends
    try:
        filtered_df = filtered_df[~filtered_df['Date'].dt.dayofweek.isin([5, 6])]
    except Exception as e:
        print(f"Error filtering weekends: {e}")
        return []

    # Sort the DataFrame by 'Date' in ascending order
    filtered_df = filtered_df.sort_values(by='Date', ascending=True)

    # Select the most recent 5 business days
    latest_five_business_days_df = filtered_df.tail(5).copy()

    # Format 'Date' to dd-mm-yyyy
    try:
        latest_five_business_days_df['Date'] = latest_five_business_days_df['Date'].dt.strftime('%d-%m-%Y')
    except Exception as e:
        print(f"Error formatting dates: {e}")
        return []

    return latest_five_business_days_df.to_dict(orient='records')

def fetch_fii_dii_data_and_format():
    data = fetch_fii_dii_data()
    final_data = data_cleaning(data)
    print("---------------------------------------------------------")
    # print(final_data)
    return final_data

# Call the function
# fetch_fii_dii_data_and_format()
