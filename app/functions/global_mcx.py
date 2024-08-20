import asyncio
import aiohttp
import random
import time
import pandas as pd

def fetch(url: str, session=None):
    user_agents = [
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Cache-Control': 'no-cache, no-store, must-revalidate',  # No cache headers
        'Pragma': 'no-cache',  # HTTP 1.0 backward compatibility
        'Expires': '0'  # Expire immediately
    }


    
def saveIndianARDData():
    url = 'https://appfeeds.moneycontrol.com/jsonapi/market/get_indian_adrs'
    data = fetch(url)
    df = pd.DataFrame(data)
    required_columns = ["shortname", "lastprice", "percentchange", "upd_epoch", "market_state"]
    df_filtered = df[required_columns]
    df_filtered = df_filtered.to_dict(orient='records')
    print(df_filtered)


def currencyData():
    url = 'https://api.moneycontrol.com/mcapi/v1/us-markets/getCurrencies'
    data = fetch(url)
    # print(data.get('data'))
    df = pd.DataFrame(data.get('data'))
    required_columns = ["name", "ltp", "chgper", "lastepoch", "market_state"]
    df_filtered = df[required_columns]
    df_filtered = df_filtered.to_dict(orient='records')
    print(df_filtered)

def mcxData():
    url = 'https://appfeeds.moneycontrol.com/jsonapi/commodity/top_commodity&ex=MCX&format=json'
    data = fetch(url)
    data = data.get('list')
    # print(data)
    df = pd.DataFrame(data)
    # print(df.columns)
    required_columns = ["id", "lastprice", "percentchange", "lastupdate", "market_state"]
    df_filtered = df[required_columns]
    df_filtered = df_filtered.to_dict(orient='records')
    print(df_filtered)

def globalFetch():
    url = 'https://priceapi.moneycontrol.com/technicalCompanyData/globalMarket/getGlobalIndicesListingData?view=overview&deviceType=W'

    data = fetch(url)
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
    
    # Filter the DataFrame to keep only the required columns
    # required_columns = ["symbol", "name", "price", "percent_change", "last_updated", "flag_url", "state"]
    required_columns = ["name", "price", "percent_change", "last_updated", "flag_url", "state"]
    df_filtered = df[required_columns]
    global_list = df_filtered.to_dict(orient='records')
    print(global_list)
    return global_list

# globalFetch()
            

