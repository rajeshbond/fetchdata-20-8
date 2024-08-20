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


router = APIRouter(
    prefix= '/live',
     tags=["Live Data"]
)


@router.get("/api/liveheat", status_code=status.HTTP_200_OK,response_model=List[schemas.Nifty50])
def liveheat(background_tasks: BackgroundTasks):
    try:
      heat_map = getIndex("NIFTY 50")
      return heat_map
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@router.post("/api/indexfetch", status_code=status.HTTP_200_OK)
def fetch_indexfetch():
    try:
        fetch_data = indexfetch()
        # print(fetch_data)
        return fetch_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "code start Running"}

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

    