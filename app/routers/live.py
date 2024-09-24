from fastapi.responses import JSONResponse
import pandas as pd
from fastapi import Response, status, HTTPException, Depends, APIRouter , BackgroundTasks
from sqlalchemy.orm import Session
from ..import schemas,models
from ..database import get_db
from typing import List
from ..functions.nse_data import market_status , getIndex , is_trading_holiday, indexfetch
from sqlalchemy import desc , text
from ..util.day import check_day # type: ignore
from fastapi.encoders import jsonable_encoder
from ..functions.money import mcxData, currencyData , saveIndianARDData, global_data
from ..functions.fiicontrol import fetch_fii_dii_data_and_format
import os , pandas as pd    
import numpy as np


router = APIRouter(
    prefix= '/live',
     tags=["Live Data"]
)


@router.post("/api/liveheat", status_code=status.HTTP_200_OK,response_model=List[schemas.Nifty50])
def liveheat(index:schemas.indexinput):
    condition_name = index.indexName
    try:
        file_name = f'heatmap/{condition_name}.csv'    
        if os.path.exists(file_name):
            heatcsv_data = pd.read_csv(file_name)
            heat_index = heatcsv_data.to_dict('records')
            return heat_index
        else:
            # old_data = pd.DataFrame(columns=['index', 'last', 'percentChange'])
            old_data = pd.DataFrame(columns=['symbol', 'lastPrice', 'pChange'])
            return old_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/indexfetch", status_code=status.HTTP_200_OK,response_model=List[schemas.allIndex])
def liveheat(index:schemas.indexinput):
    condition_name = index.indexName
    try:
        file_name = f'heatmap/{condition_name}.csv'    
        if os.path.exists(file_name):
            heatcsv_data = pd.read_csv(file_name)
            all_index = heatcsv_data.to_dict('records')
            return all_index
        else:
            old_data = pd.DataFrame(columns=['index', 'last', 'percentChange'])
            return old_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/api/indexfetch_heat", status_code=status.HTTP_200_OK,response_model=List[schemas.allIndex])
def liveheat(index:schemas.indexinput):
    condition_name = index.indexName
    try:
        file_name = f'heatmap/{condition_name}.csv'    
        if os.path.exists(file_name):
            heatcsv_data = pd.read_csv(file_name)
            all_index = heatcsv_data.to_dict('records')
            return all_index
        else:
            print("File not found")
            old_data = pd.DataFrame(columns=['index', 'last', 'percentChange'])
            return old_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/board_meeting", status_code=status.HTTP_200_OK)
def liveheat(index:schemas.indexinput):
    condition_name = index.indexName
    try:
        file_name = f'FetchedData/{condition_name}.csv'    
        if os.path.exists(file_name):
            heatcsv_data = pd.read_csv(file_name)
            all_index = heatcsv_data.to_dict('records')
            return all_index
        else:
            old_data = pd.DataFrame(columns=['bm_symbol', 'bm_purpose', 'bm_desc','bm_date', 'bm_timestamp','attachment'])
            return old_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/ipo", status_code=status.HTTP_200_OK)
def liveheat(index: schemas.indexinput):
    condition_name = index.indexName
    try:
        file_name = f'FetchedData/{condition_name}.csv'
        if os.path.exists(file_name):
            heatcsv_data = pd.read_csv(file_name)
            
            # Replace inf and -inf with None
            heatcsv_data.replace([float('inf'), -float('inf')], None, inplace=True)
            
            # Convert DataFrame to dictionary
            data_dict = heatcsv_data.to_dict('records')
            # print(data_dict)
            # Explicitly handle NaN values in the dictionary
            for record in data_dict:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
            
            # print(data_dict)
            
            return data_dict
        else:
            old_data = pd.DataFrame(columns=['symbol', 'companyName', 'series', 'issueStartDate', 'issueEndDate', 'status', 'issueSize', 'issuePrice', 'sr_no', 'isBse', 'lotSize', 'priceBand'])
            return old_data.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    

@router.post("/api/fii", status_code=status.HTTP_200_OK)
def fetch_fii():
    try:
        fiiData = fetch_fii_dii_data_and_format()
        return fiiData
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  


@router.post("/api/commodity", status_code=status.HTTP_200_OK,response_model=List[schemas.Commodity])
def fetch_commodity():  
    try:    
        com = mcxData()
        return com
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/api/currency", status_code=status.HTTP_200_OK,response_model=List[schemas.Currency])
def fetch_currency():
    try:
        currency = currencyData()
        return currency
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/api/ard", status_code=status.HTTP_200_OK,response_model=List[schemas.IndianARD])
def fetch_ard():
    try:
        ard = saveIndianARDData()
        return ard
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/globalstatus", status_code=status.HTTP_200_OK,response_model=List[schemas.GlobalData])
def fetch_global_status():
    try:
        global_status = global_data()
        return global_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/block_deals", status_code=status.HTTP_200_OK)
def block_deals(index:schemas.indexinput):
    condition_name = index.indexName
    # print(condition_name)
    try:
        file_name = f'FetchedData/{condition_name}.csv'
        
        if os.path.exists(file_name):
            newscsv_data = pd.read_csv(file_name)

            # Replace NaN, inf, -inf with None
            newscsv_data = newscsv_data.replace([np.inf, -np.inf], np.nan)
            newscsv_data = newscsv_data.where(pd.notnull(newscsv_data), None)

            # Ensure conversion of any problematic data types into JSON-compliant ones
            newscsv = newscsv_data.astype(object).where(pd.notnull(newscsv_data), None).to_dict(orient='records')
            
            return JSONResponse(content=newscsv)
        
        else:
            # Return an empty structure if the file does not exist
            empty_data = pd.DataFrame(columns=['date', 'symbol', 'clientName', 'buySell', 'qty', 'watp', 'remarks'])
            return JSONResponse(content=empty_data.to_dict('records'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/day_block", status_code=status.HTTP_200_OK)
def day_block(index:schemas.indexinput):
    condition_name = index.indexName
    # print(condition_name)
    try:
        file_name = f'FetchedData/{condition_name}.csv'
        
        if os.path.exists(file_name):
            newscsv_data = pd.read_csv(file_name)
            newscsv = newscsv_data.to_dict(orient='records')
            # print(newscsv)
            return JSONResponse(content=newscsv)
        
        else:
            # Return an empty structure if the file does not exist
            empty_data = pd.DataFrame(columns=['session', 'symbol', 'series', 'open','dayHigh', 'dayLow', 'lastPrice', 'previousClose','pchange','totalTradedVolume','totalTradedValue','lastUpdateTime','exDate'])
            return JSONResponse(content=empty_data.to_dict('records'))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/news", status_code=status.HTTP_200_OK)
def top_news(index:schemas.indexinput):
    condition_name = index.indexName
    # print(condition_name)
    try:
        file_name = f'edgeData/{condition_name}.csv'
        
        if os.path.exists(file_name):
            newscsv_data = pd.read_csv(file_name)
            newscsv = newscsv_data.to_dict(orient='records')
            # print(newscsv)
            return newscsv
            # return JSONResponse(content=newscsv)
        
        else:
            # Return an empty structure if the file does not exist
            empty_data = pd.DataFrame(columns=['Date', 'Description', 'Description'])
            return JSONResponse(content=empty_data.to_dict('records'))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))