import time, os
import requests
from fastapi import Response, status, HTTPException, Depends, APIRouter
from bs4 import BeautifulSoup as bs
import pandas as pd
import pytz,os, datetime
import asyncio
from pprint import pprint
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from sqlalchemy import text, column
from sqlalchemy.sql import select
from .sorted_data import frequency
from .comp import compare_csv_files

# from fetch_data import nse_data

# from google_sheet import clean_up, update_google_sheet,update_cell
# t.me/CompoundingFunda_bot
URL = 'https://chartink.com/screener/process'

def scandata(condition, conditionName):
    try:
        db = next(get_db())
        symbol_df = pd.read_sql(db.query(models.Symbol).statement, db.bind)
        directory = 'mid'
        with requests.session() as s:
            rawData = s.get(URL)
            soup = bs(rawData.content, "lxml")
            meta = soup.find('meta', {"name": "csrf-token"})['content']
            header = {"X-Csrf-Token": meta}
            responseData_scan1 = s.post(url=URL, headers=header, data=condition, timeout=10000)
            if responseData_scan1.content:
                data = responseData_scan1.json()
                stock = data['data']
                stock_list = pd.DataFrame(stock)
                print(f"-------------------{conditionName}----------------------------")
                print(stock_list)
                if stock_list.empty:
                    time.sleep(2)
                    df_empty = pd.DataFrame(columns=['nsecode', 'per_chg', 'close','date','igroup_name'])
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    # print("no data")
                    df_empty.to_csv(f'mid/{conditionName}.csv', index=False)
                    return pd.DataFrame(columns=['nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume', 'date', 'time', 'igroup_name'])

                today = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).date())
                stock_list['date'] = today
                now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))  
                current_time = now.strftime('%H:%M:%S')
                stock_list['time'] = str(current_time)
                stock_list['nsecode'] = stock_list['nsecode'].fillna('NA')
                stock_list['bsecode'] = stock_list['bsecode'].fillna(0)
                datafile = pd.merge(stock_list,  symbol_df[["nsecode", 'igroup_name']], on="nsecode", how='left')
                datafile['igroup_name'] = datafile['igroup_name'].fillna('Others')
                # print(datafile)
              
                new_data = datafile.drop(['sr','name','bsecode','volume','time'],axis=1)
                # print(new_data)
                file_name = f'mid/{conditionName}.csv'    
                if os.path.exists(file_name):
                    old_data = pd.read_csv(f'mid/{conditionName}.csv')
                else:
                    old_data = pd.DataFrame(columns=['nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume', 'date', 'time', 'igroup_name'])
                    # print(old_data)
                old_data = old_data.drop(columns=['date'])
                new_data_with_date = new_data.drop(columns=['date'])
                comp_result = compare_csv_files(old_data , new_data_with_date)
                # print(f"------- Comparison result for {conditionName} --> {comp_result}<--888888888888")
                
                # directory = 'mid'
                if comp_result:
                    # print(f"Data already exists in mid/{conditionName}.csv")
                    # print("no data")
                    return pd.DataFrame(columns=['nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume', 'date', 'time', 'igroup_name'])
                else:
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    # print(f"saving data to mid/{conditionName}.csv")
                    new_data.to_csv(f'mid/{conditionName}.csv', index=False)
                    # dayStockSelector(datafile)
                    # nse_data()
                    return datafile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return pd.DataFrame(columns=['nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume', 'date', 'time', 'igroup_name'])
    
def chartinkLogicBankend(condition, conditionName, db_name):
    try:
        today = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).date())
        db = next(get_db())

        model_mapping = {
            ("IntradayData", "Champions Intraday"): models.IntradayData,
            ("OverBroughtData", "Champions Over Brought"): models.OverBroughtData,
            ("PositionalData", "Champions Positional"): models.PositionalData,
            ("ReversalData", "Champions Reversal Stocks"): models.ReversalData,
            ("SwingData", "Champions Swing"): models.SwingData,
            ("Condition6", "Champions Condition 6"): models.Condition6
        }

        model_class = model_mapping.get((db_name, conditionName))
        
        if not model_class:
            # print(f"No model mapping found for {db_name} and {conditionName}")
            return

        scandataFunc_df = scandata(condition, conditionName)

      

        # print(f"Dataframe columns from scandata: {scandataFunc_df.columns}")
        selected_columns = ['nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume', 'date', 'time', 'igroup_name']
        newScandataFunc = scandataFunc_df[selected_columns]

        existing_data = pd.read_sql(db.query(model_class).statement, db.bind)
        if scandataFunc_df.empty:
            frequency(existing_data, conditionName)
            # print(f"{db_name} {conditionName} data not found in scan")
            return
        
        if not existing_data.empty:
            frequency(existing_data, conditionName)
            new_data = newScandataFunc[~newScandataFunc['nsecode'].isin(existing_data.loc[existing_data['date'] == today, 'nsecode'])]

            if new_data.empty:
                # print(f"No new data found for {conditionName}")
                return
            else:
                # print(f"New data found for {conditionName}, adding to database {db_name}...")
                new_entries = new_data.to_dict(orient='records')
                try:
                    db.bulk_insert_mappings(model_class, new_entries)
                    db.commit()
                except Exception as e:
                    print(f"{conditionName} ---> error {e}")
        else:
            # print(f"{db_name} {conditionName} data not found in database")
            # print(f"Entering the {conditionName} to database {db_name}...")
            data_to_insert = newScandataFunc.to_dict(orient='records')
            try:
                db.bulk_insert_mappings(model_class, data_to_insert)
                db.commit()
            except Exception as e:
                print(f"{conditionName} ---> error {e}")

    except Exception as e:
        print(f"Error in chartinkLogicBankend: {e}")




# def chartinkLogicBankend(condition, conditionName,db_name):
#     try:
#         # today = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).date())
#         scandata(condition, conditionName)
#         # Fetch a database session
#         db = next(get_db())
        
        # frequency(intra_data,conditionName)
        
        # For Indraday Condition --- start
        # Previous code ---------Starts
        # if (db_name == "IntradayData" and conditionName == "Champions Intraday"):
        #     intra_data = pd.read_sql(db.query(models.IntradayData).statement, db.bind)
           
            
                
        # # For OverBroughtData Condition --- start
        # elif (db_name == "OverBroughtData" and conditionName == "Champions Over Brought"):
         
       
        #     over_brought_data = pd.read_sql(db.query(models.OverBroughtData).statement, db.bind)
        #     if over_brought_data.empty:
        #         print(f"{db_name} {conditionName}data not found in scan")
        #         return
        #     frequency(over_brought_data,conditionName)
           
        # # For PositionalData Condition --- start  
        # elif (db_name == "PositionalData" and conditionName == "Champions Positional"):
        #     positonal_data = pd.read_sql(db.query(models.PositionalData).statement, db.bind)
        #     if positonal_data.empty:
        #         print(f"{db_name} {conditionName}data not found in scan")
        #         return
        #     frequency(positonal_data,conditionName)
            
        # elif (db_name == "ReversalData" and conditionName == "Champions Reversal Stocks"):  
        #     reversal_data = pd.read_sql(db.query(models.ReversalData).statement, db.bind)
        #     if reversal_data.empty:
        #         print(f"{db_name} {conditionName}data not found in scan")
        #         return
        #     frequency(reversal_data,conditionName)
            
        # elif (db_name == "SwingData" and conditionName == "Champions Swing"):
        #     swing_data = pd.read_sql(db.query(models.SwingData).statement, db.bind)
        #     if swing_data.empty:
        #         print(f"{db_name} {conditionName}data not found in scan")
        #         return
        #     frequency(swing_data,conditionName)
                
                
        # else:
        #     return
        # Previous code ---------
    # except Exception as e:
    #     print(f"chartinkLogicBankend error: {e}")


    
# def dayStockSelector(scanData):
#     # print("-----------dayStockSelector------------")
#     # print(scanData['nsecode'])
#     db = next(get_db())
#     day_symbol = pd.read_sql(db.query(models.DaySymbol).statement, db.bind)

#     if not day_symbol.empty:
#         new_symbol_entry = scanData[~scanData['nsecode'].isin(day_symbol['nsecode'])]

#         if new_symbol_entry.empty:
#             print("No new data found")
#             return
#         print("New data found")
#         print(new_symbol_entry)
#         new_symbol_entry = new_symbol_entry.to_dict(orient='records')
#         print("---------------New data found-------------\n")
#         try:
#             db.bulk_insert_mappings(models.DaySymbol, new_symbol_entry)
#             db.commit()
#             pass
#         except Exception as e:
#             print(f"dayStockSelector error in dataBase (e)")
#             raise HTTPException(status_code=500, detail=str(e))
#     else:
#         try:
#             new_symbol_entry = scanData
#             print("---------------First Entry -------------\n")
#             print(new_symbol_entry)
#             new_symbol_entry = scanData.to_dict(orient='records')
            
#             db.bulk_insert_mappings(models.DaySymbol, new_symbol_entry)
#             db.commit()
#         except Exception as e:
#             print(f"dayStockSelector error in dataBase (e)")
#             raise HTTPException(status_code=500, detail=str(e))