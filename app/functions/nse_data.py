from jugaad_data.nse import NSELive
import pandas as pd
from fastapi import HTTPException
from datetime import datetime
import pytz
n = NSELive()


def market_status():
  status = n.market_status()
  data =status['marketState'][0]['marketStatus']
  return data

market_status()

def getIndex(index_name):
  index = n.live_index(index_name)
  data = index['data']
  df = pd.DataFrame(data)
  df = df[['symbol', 'lastPrice', 'pChange']]
  df = df.sort_values(by='pChange', ascending=False)
  df = df.drop(0)
  df_dict = df.to_dict('records')
  # print(df_dict)
  return df_dict

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
      # print("hello")
      index = n.all_indices()
      data = index['data']
      df = pd.DataFrame(data)
      df = df[['index', 'last', 'percentChange']]
      list_df = df.to_dict('records')
      return list_df
    #   print(list_df)
   except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
# Example usage

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

def mostActive():
   active = n.trade_info("SBIN")
   print(active)

# mostActive()
# donutChart()