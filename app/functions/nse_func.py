from .nse_rajesh import fetch_nse_data
import pandas as pd, os
from datetime import datetime 
import time
directory = 'FetchedData'

def fii():
    api_url = "https://www.nseindia.com/api/fiidiiTradeReact"
    data = fetch_nse_data(api_url)

    if data:
        print(data)
        return data
    else:
        print("Failed to retrieve data.")
  
# fii()

def corporate_analytics():
    api_url = "https://www.nseindia.com/api/home-corporate-announcements?index=homepage"
    # api_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
    data = fetch_nse_data(api_url)
    # print(data)
    data = data.get('data')
    # print(data)
    if data:
        df = pd.DataFrame(data)
        list = df.to_dict('records')
        print(list)
        return list
    else:
        print("Failed to retrieve data.")

# corporate_analytics()

def block_deals():
    api_url = "https://www.nseindia.com/api/block-deal"
    data = fetch_nse_data(api_url)
    data = data['data']
    # print(data)
    try:
        if data:
            df = pd.DataFrame(data)
            # print(df)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if data:
                df = pd.DataFrame(data)
                # list = df.to_dict('records')
                # print(list)
                df.to_csv(f'{directory}/day_block.csv', index=False)
            
            return list
        else:
            empty_data = pd.DataFrame(columns=['session', 'symbol', 'series', 'open','dayHigh', 'dayLow', 'lastPrice', 'previousClose','pchange','totalTradedVolume','totalTradedValue','lastUpdateTime','exDate', 'Description'])
            empty_data.to_csv(f'{directory}/day_block.csv', index=False)
            # print("Failed to retrieve data.")
    except Exception as e:
        print(e)
# block_deals()

def bulk_deals():
    api_url = "https://www.nseindia.com/api/snapshot-capital-market-largedeal"
    data = fetch_nse_data(api_url)
    data = data.get('BLOCK_DEALS_DATA')
    # print(data)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if data:
        df = pd.DataFrame(data)
        list = df.to_dict('records')
        # print(list)
        df.to_csv(f'{directory}/done_block.csv', index=False)

# bulk_deals()

def current_ipo():
    api_url = "https://www.nseindia.com/api/ipo-current-issue"
    # api_url = "https://www.nseindia.com/api/all-upcoming-issues?category=ipo"
    data = fetch_nse_data(api_url)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if data:
        df = pd.DataFrame(data)
        current_date = datetime.now().strftime('%d-%b-%Y')
        df['issueEndDate'] = pd.to_datetime(df['issueEndDate'], format='%d-%b-%Y')
        # active_ipos = df[(df['issueEndDate'] >= pd.to_datetime(current_date)) & (df['status'] == 'Active')]
        active_ipos = df[(df['issueEndDate'] >= pd.to_datetime(current_date))]
        active_ipos = active_ipos.sort_values(by='issueEndDate', ascending=True)
        active_ipos.to_csv(f'{directory}/ipo.csv', index=False)
        # print(active_ipos.to_dict('records'))
    else:
        print("Failed to retrieve data.")

# current_ipo()

def corporate_announcements():
    api_url = "https://www.nseindia.com/api/home-corporate-actions?index=equities"
    data = fetch_nse_data(api_url)
    print(data.get('data'))

# corporate_announcements()

def board_meetings():
    api_url = "https://www.nseindia.com/api/home-board-meetings?index=equities"
    data = fetch_nse_data(api_url)
    data = data.get('data')
    print(data)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if data:
        df = pd.DataFrame(data)
        # list = df.to_dict('records')
        print(list)
        df.to_csv(f'{directory}/board_meetings.csv', index=False)
    else:
        print("Failed to retrieve data.")

def market_status_1():
    api_url = "https://www.nseindia.com/api/marketStatus"
    data = fetch_nse_data(api_url)
    data = data.get('marketState')
    data = data[0]['marketStatus']
    print(data)

def fetch_nifty_data_index(url, index_name):
    # api_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
    api_url = url
    data = fetch_nse_data(api_url)
    data = data.get('data')
    data = pd.DataFrame(data)
    data = data.drop(0)
    # data = data[data['priority'] != 1]
    data = data[['symbol','lastPrice', 'pChange']]
    nifty50_df = data.sort_values(by='pChange', ascending=False)
    print(nifty50_df)
    if not os.path.exists(directory):
          os.makedirs(directory)
    if nifty50_df.empty:
        nifty50_df = pd.DataFrame(columns=['symbol', 'lastPrice', 'pChange'])
        nifty50_df.to_csv(f'{directory}/{index_name}.csv', index=False)
    else:
        nifty50_df.to_csv(f'{directory}/{index_name}.csv', index=False)
        print(nifty50_df.to_dict('records')) 



# fetch_nifty_data_index("https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050", fileName="nifty50")   
# fetch_nifty_data_index("https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK", index_name="NIFTY BANK")   

# count = 1
# while True:
#     fetch_nifty_50()
#     print(f"=========={count}===========")
#     count += 1
#     time.sleep(0.5)