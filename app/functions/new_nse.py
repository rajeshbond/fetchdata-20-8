from fastapi import HTTPException
from .nse_rajesh import fetch_nse_data
import pandas as pd, os
from datetime import datetime 
import time
directory = 'heatmap'


def market_status_1():
    api_url = "https://www.nseindia.com/api/marketStatus"
    data = fetch_nse_data(api_url)
    data = data.get('marketState')
    data = data[0]['marketStatus']
    return data

def fetch_nifty_data_index(url, index_name):
    api_url = url
    data = fetch_nse_data(api_url)
    data = data.get('data')
    data = pd.DataFrame(data)
    data = data.drop(0)
    # data = data[data['priority'] != 1]
    data = data[['symbol','lastPrice', 'pChange']]
    nifty50_df = data.sort_values(by='pChange', ascending=False)
    # print(nifty50_df)
    if not os.path.exists(directory):
          os.makedirs(directory)
    if nifty50_df.empty:
        nifty50_df = pd.DataFrame(columns=['symbol', 'lastPrice', 'pChange'])
        nifty50_df.to_csv(f'{directory}/{index_name}.csv', index=False)
    else:
        nifty50_df.to_csv(f'{directory}/{index_name}.csv', index=False)
        # print(nifty50_df.to_dict('records')) 

def indexes_all():
    try:
      api_url = "https://www.nseindia.com/api/allIndices"
      data = fetch_nse_data(api_url)
      data = data.get('data')
      data = pd.DataFrame(data)
      index_df = data[['index','last', 'percentChange']]
      custom_sequence = [
            'NIFTY 50', 'NIFTY NEXT 50', 'NIFTY 100', 'NIFTY 200', 
            'NIFTY 500', 'NIFTY BANK', 'NIFTY IT', 'NIFTY REALTY', 'NIFTY AUTO', 
            'NIFTY PHARMA', 'NIFTY FIN SERVICE', 'NIFTY METAL', 'NIFTY CONSR DURBL', 
            'NIFTY COMMODITIES', 'NIFTY ENERGY', 'NIFTY OIL AND GAS', 
            'NIFTY HEALTHCARE', 'NIFTY PSU BANK', 'NIFTY PVT BANK', 
            'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100', 'NIFTY SMLCAP 100','NIFTY MEDIA','INDIA VIX'
      ]
      if custom_sequence:
        index_df = index_df.set_index('index')

              # Reindex to match custom_sequence, keeping only valid ones
        index_df = index_df.reindex(custom_sequence).dropna().reset_index()

      # print(index_df)
      if not os.path.exists(directory):
        os.makedirs(directory)

      if index_df.empty:
        index_df = pd.DataFrame(columns=['index', 'last', 'percentChange'])
        index_df.to_csv(f'{directory}/all_indices.csv', index=False)
      else:
          # Save DataFrame to CSV
        # csv_file = os.path.join(directory, 'all_indices.csv')
        index_df.to_csv(f'{directory}/all_indices.csv', index=False)
      
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  
    


