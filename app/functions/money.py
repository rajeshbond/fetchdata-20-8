import os
import requests
import pickle
import random
import pandas as pd
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

@cached("nse_cache", timeout=3600)  # 1 hour timeout
def fetch_control(url):
    # Rotate User-Agent for each request
    headers = {
        'User-Agent': random.choice(user_agents),
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.moneycontrol.com/'
    }

    # Initial request to fetch cookies (replace with the actual URL that sets the cookies)
    initial_url = "https://www.moneycontrol.com/"
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
    

def mcxData():
    url = 'https://appfeeds.moneycontrol.com/jsonapi/commodity/top_commodity&ex=MCX&format=json'
    data = fetch_control(url)
    data = data.get('list')
    # print(data)
    df = pd.DataFrame(data)
    # print(df.columns)
    required_columns = ["id", "lastprice", "percentchange", "lastupdate", "market_state"]
    df_filtered = df[required_columns]
    df_filtered = df_filtered.to_dict(orient='records')
    # print(df_filtered)
    return df_filtered

def currencyData():
    url = 'https://api.moneycontrol.com/mcapi/v1/us-markets/getCurrencies'
    data = fetch_control(url)
    df = pd.DataFrame(data.get('data'))
    required_columns = ["name", "ltp", "chgper", "lastepoch", "market_state"]
    df_filtered = df[required_columns]
    df_filtered = df_filtered.to_dict(orient='records')
    return df_filtered

def saveIndianARDData():
    url = 'https://appfeeds.moneycontrol.com/jsonapi/market/get_indian_adrs'
    data = fetch_control(url)
    df = pd.DataFrame(data)
    required_columns = ["shortname", "lastprice", "percentchange", "upd_epoch", "market_state"]
    df_filtered = df[required_columns]
    df_filtered = df_filtered.to_dict(orient='records')
    # print(df_filtered)
    return df_filtered

def global_data():
    url = 'https://priceapi.moneycontrol.com/technicalCompanyData/globalMarket/getGlobalIndicesListingData?view=overview&deviceType=W'

    data = fetch_control(url)
    print(data)
    if data is None:
        print("No data to process.")
        return

    data_list = data.get("dataList", [])
    all_rows = []
    
    # Iterate through categories and collect data
    for category in data_list:
        category_data = category.get("data", [])
        all_rows.extend(category_data)  # Collect all rows from each category

    # Define column names as per the response
    columns = ["symbol", "name", "price", "net_change", "percent_change", "high", "low", "open", "prev_close", "52wkHigh", "52wkLow", "weekly_per_change", "monthly_per_change", "3months_per_change", "6months_per_change", "ytd_per_change", "yearly_per_change", "2years_per_change", "3years_per_change", "5years_per_change", "technical_rating", "last_updated", "flag_url", "state", "isDerived", "link_flag", "message"]
    
    # Create a DataFrame from the collected rows
    df = pd.DataFrame(all_rows, columns=columns)
    
   
    required_columns = ["name", "price", "percent_change", "last_updated", "flag_url", "state"]
    df_filtered = df[required_columns]
    global_list = df_filtered.to_dict(orient='records')
    print(global_list)
    return global_list

# global_data()

