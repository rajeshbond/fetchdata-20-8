
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from fastapi import Response, status, HTTPException, Depends, APIRouter
import json
from datetime import datetime, time , timedelta
import requests, time
import pandas as pd
from sqlalchemy import func


def datetotimestamp(date):
        # time_tuple = date.timetuple()
        # timestamp = round(time.mktime(date.time_tuple))
        return round(time.mktime(date.timetuple()))
def timestamptodate(timestamp):
        return datetime.fromtimestamp(timestamp)


router = APIRouter(
    prefix= '/stock_price',
     tags=["Stock_price"]
)



# Historical Data
@router.post("/historical")
def price_entery(db: Session = Depends(get_db)):
        
        rows_query = db.query(models.Symbol).all()
        
        for row in rows_query:
                print(f"{row.id} {row.symbol} \n ")
                time_frame = 60
                start = datetotimestamp(datetime(2022,1,1))
                end = datetotimestamp(datetime.now())
                try:
                       
                        url = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol='+(row.symbol)+'&resolution='+str(time_frame)+'&from='+str(time_frame)+'&to='+str(end)+'&countback=329&currencyCode=INR'

                        payload={}
                        headers = {
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
                        }

                        data = requests.request("GET", url, headers=headers, data=payload).json()

                        print(data)
                        try: 
                                for i in range(len(data['t'])):
                                        print(data['t'][i])
                                        in_intraday = db.query(models.StockPrice).filter(models.StockPrice.date_stamp == data['t'][i], models.StockPrice.stock_id == row.id).first()
                                        if in_intraday:
                                                price("=============Already in database ")
                                        if data['s'] == 'ok'and not in_intraday:
                                                print("""""""""""""""""""""""""""""")
                                                price = {
                                                                "stock_id": row.id,
                                                                "date_stamp":data['t'][i],
                                                                "open":data['o'][i],
                                                                "high":data['h'][i],
                                                                "low":data['l'][i],
                                                                "close":data['c'][i],
                                                                "volume":data['v'][i],
                                                                
                                                }
                                                
                                        

                                                records = models.StockPrice(**price)
                                                db.add(records)
                                                db.commit()
                                                print(price)
                        except:
                                with open("missing_entry.txt","a") as file :
                                        file.write(f"{i}-->{row.id} --> {row.symbol} ---> {url} \n ")
                               
                except:
                        
                        with open("missing_symbols.txt","a") as file :
                                file.write(f"{row.id}-->{row.symbol} \n ")
                                
                        print(row.symbol)
                        pass
                                
        
        return rows_query
        

@router.post("/test/{id}")
def price_entery(id : int,db: Session = Depends(get_db)):
        
    
        # symbol = ("reliance").upper()
        time_frame = 60
        start = datetotimestamp(datetime(2022,1,1))
        end = datetotimestamp(datetime.now())
        try:
        
                url = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol={id}&resolution='+str(time_frame)+'&from='+str(start)+'&to='+str(end)+'&countback=93&currencyCode=INR'

                payload={}
                headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
                }

                data = requests.request("GET", url, headers=headers, data=payload)
                data = requests.get(url).json()
                print(data)
                try: 
                        for i in range(len(data['t'])):
                                if data['s'] == 'ok':                                        
                                        price = {
                                                        "stock_id": id,
                                                        "date_stamp":data['t'][i],
                                                        "open":data['o'][i],
                                                        "high":data['h'][i],
                                                        "low":data['l'][i],
                                                        "close":data['c'][i],
                                                        "volume":data['v'][i],   
                                        }
                                        records = models.StockPrice(**price)
                                        db.add(records)
                                        db.commit()
                                        print(price)
                except:
                        pass
        except:
                pass
              

      
        return price



@router.post("/mytest")
def price_entery_test(db: Session = Depends(get_db)):
        print('=========================================')

        url = "https://priceapi.moneycontrol.com/techCharts/intra?symbol=TCS&resolution=1&from=1681376115&to=1681376355"

        payload={}
        headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

