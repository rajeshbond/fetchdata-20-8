from jugaad_data.nse import NSELive
import pandas as pd
from fastapi import HTTPException
from datetime import datetime
import pytz, os
n = NSELive()
directory = 'heatmap'


def market_status():
  status = n.market_status()
  print(status)
  data =status['marketState'][0]['marketStatus']
  print(data)
  return data


def getIndex(index_name):
  try:
    index = n.live_index(index_name)
    data = index['data']
    nifty50_df = pd.DataFrame(data)
    nifty50_df = nifty50_df[['symbol', 'lastPrice', 'pChange']]
    nifty50_df = nifty50_df.sort_values(by='pChange', ascending=False)
    nifty50_df = nifty50_df.drop(0)
    if not os.path.exists(directory):
          os.makedirs(directory)
    if nifty50_df.empty:
        nifty50_df = pd.DataFrame(columns=['symbol', 'lastPrice', 'pChange'])
        nifty50_df.to_csv(f'{directory}/{index_name}.csv', index=False)
    else:
        nifty50_df.to_csv(f'{directory}/{index_name}.csv', index=False)
        print(nifty50_df.to_dict('records'))    
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


def nseHoildays():
    holidays = n.holiday_list()
    fo_holidays = holidays.get('FO', [])  # Assuming 'FO' is the correct key for your holiday list
    print("FO Holidays data:", fo_holidays)  # Debugging output
    return fo_holidays

def is_trading_holiday():
    # Set timezone to IST
    ist = pytz.timezone('Asia/Kolkata')
    # Get today's date in the same format as the holiday data
    today = datetime.now(ist).strftime('%d-%b-%Y')
    
    # Fetch holiday data
    holiday_data = nseHoildays()
    
    # Convert holiday data directly to a pandas DataFrame
    df = pd.DataFrame(holiday_data)
    
    # Debug: Print the DataFrame and its columns
    print(df)
    # print("Columns in DataFrame:", df.columns)
    
    # Check if today is Saturday or Sunday
    weekday = datetime.now(ist).weekday()  # Monday is 0 and Sunday is 6
    if weekday == 5:
        print("Today is Saturday, hence it's a trading holiday.")
        return True
    elif weekday == 6:
        print("Today is Sunday, hence it's a trading holiday.")
        return True

    # Check if today's date is in the 'tradingDate' column
    if today in df['tradingDate'].values:
        holiday = df[df['tradingDate'] == today].iloc[0]
        print(f"Today is a trading holiday: {holiday['description']}")
        return True
    
    print("Today is not a trading holiday.")
    return False

def indexfetch():
    try:
        # Fetch all indices data
        index = n.all_indices()
        data = index['data']

        # Convert the data to a DataFrame and select relevant columns
        index_df = pd.DataFrame(data)
        index_df = index_df[['index', 'last', 'percentChange']]

        # Sort by 'percentChange' in descending order first
        # index_df = index_df.sort_values(by='percentChange', ascending=False)

        # Custom sequence (user-defined order of indices)
        custom_sequence = [
            'NIFTY 50', 'NIFTY NEXT 50', 'NIFTY 100', 'NIFTY 200', 
            'NIFTY 500', 'NIFTY BANK', 'NIFTY IT', 'NIFTY REALTY', 'NIFTY AUTO', 
            'NIFTY PHARMA', 'NIFTY FIN SERVICE', 'NIFTY METAL', 'NIFTY CONSR DURBL', 
            'NIFTY COMMODITIES', 'NIFTY ENERGY', 'NIFTY OIL AND GAS', 
            'NIFTY HEALTHCARE', 'NIFTY PSU BANK', 'NIFTY PVT BANK', 
            'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100', 'NIFTY SMLCAP 100','NIFTY MEDIA','INDIA VIX'
        ]

        # Apply the custom sequence if provided
        if custom_sequence:
            index_df = index_df.set_index('index')

            # Reindex to match custom_sequence, keeping only valid ones
            index_df = index_df.reindex(custom_sequence).dropna().reset_index()


        # index_df = index_df.sort_values(by='percentChange', ascending=False) 

        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save DataFrame to CSV
        csv_file = os.path.join(directory, 'all_indices.csv')
        index_df.to_csv(csv_file, index=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def donutChart():
  try:
    donutindex = n.all_indices()
    data = donutindex['data']
    df = pd.DataFrame(data)
    df = df[['index', 'last', 'percentChange','declines','advances','advances']]
    df = df.head(20)
    list_donut = df.to_dict('records')
    print(list_donut)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


def indexfetch_heat():
    try:
        # Fetch all indices data
        index = n.all_indices()
        data = index['data']

        # Convert the data to a DataFrame and select relevant columns
        index_df = pd.DataFrame(data)
        index_df = index_df[['index', 'last', 'percentChange']]

        # Sort by 'percentChange' in descending order first
        # index_df = index_df.sort_values(by='percentChange', ascending=False)

        # Custom sequence (user-defined order of indices)
        custom_sequence = [
            'NIFTY 50', 'NIFTY NEXT 50', 'NIFTY 100', 'NIFTY 200', 
            'NIFTY 500', 'NIFTY BANK', 'NIFTY IT', 'NIFTY REALTY', 'NIFTY AUTO', 
            'NIFTY PHARMA', 'NIFTY FIN SERVICE', 'NIFTY METAL', 'NIFTY CONSR DURBL', 
            'NIFTY COMMODITIES', 'NIFTY ENERGY', 'NIFTY OIL AND GAS', 
            'NIFTY HEALTHCARE', 'NIFTY PSU BANK', 'NIFTY PVT BANK', 
            'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100', 'NIFTY SMLCAP 100','NIFTY MEDIA','INDIA VIX'
        ]

        # Apply the custom sequence if provided
        if custom_sequence:
            index_df = index_df.set_index('index')

            # Reindex to match custom_sequence, keeping only valid ones
            index_df = index_df.reindex(custom_sequence).dropna().reset_index()


        index_df = index_df.sort_values(by='percentChange', ascending=False) 

        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save DataFrame to CSV
        csv_file = os.path.join(directory, 'all_indices_heat.csv')
        index_df.to_csv(csv_file, index=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# market_status()
