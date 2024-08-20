import time
from fastapi import HTTPException,status
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from .back_end_chart_ink import chartinkLogicBankend

from .nse_data import market_status




def trasferDataToGoogleSheet():

    # URL = 'https://chartink.com/screener/process'
    URL = 'https://chartink.com/widget/process'

    # Initialize prev_data as None before the loop
    # print("started")
    count = 0
    test = 1
    
    while True:
        test = 0
        market = market_status()
        # print(market)
        # updatenseIndex()
        # marketAdvacneDecline()
        # if(market == 'Closed' or market == "Close"):
        #     # print(f"Market is {market}")
        #     return HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail="Market Closed")
            
        try:
            title = "Champions Screener"
            sub_title = "powered by SnT Solution - 8080105062"
            # update_cell(cell='A3',data=title,sheetname='Champions DashBoard')
            # update_cell(cell='A200',data=sub_title,sheetname='DashBoard')
            # Condtion 1
            conditionName = "Champions Intraday" # change name Here
            conditionNameLocation = "A4"
            db_name = "IntradayData"
            # Put condition here
            CONDITION1 = {"scan_clause": "( {cash} ( ( {57960} ( ( {cash} ( latest cci( 20 ) >= -100 and weekly cci( 20 ) >= -150 and latest rsi( 14 ) > 30 and weekly rsi( 14 ) >= 45 and monthly rsi( 14 ) >= 50 and market cap > 250 and latest obv >= [0] 4 hour obv and latest macd line( 13 , 8 , 5 ) >= [0] 15 minute macd line( 13 , 8 , 5 ) and weekly obv >= 1 week ago obv and latest avg true range( 14 ) >= 1 day ago avg true range( 14 ) and weekly avg true range( 14 ) >= 1 week ago avg true range( 14 ) and latest rsi( 14 ) >= 1 day ago rsi( 14 ) ) ) ) ) ) )"}
            # CONDITION1 = {"scan_clause": "( {cash} ( ( {57960} ( ( {cash} ( latest cci( 20 ) >= -100 and weekly cci( 20 ) >= -150 and latest rsi( 14 ) > 30 and weekly rsi( 14 ) >= 45 and monthly rsi( 14 ) >= 50 and market cap > 250 and latest obv >= [0] 4 hour obv and latest macd line( 13 , 8 , 5 ) >= [0] 5 minute macd line( 13 , 8 , 5 ) and weekly obv >= 1 week ago obv and latest avg true range( 14 ) >= 1 day ago avg true range( 14 ) and weekly avg true range( 14 ) >= 1 week ago avg true range( 14 ) and latest rsi( 14 ) >= 1 day ago rsi( 14 ) ) ) ) ) ) )"}
            # 
            row_to_start ='A3'
            row_to_clean = 'A3:D'
            chartinkLogicBankend(condition=CONDITION1 ,conditionName=conditionName,db_name=db_name)

        except Exception as e:
            print(e)
        # Condtion 2
        try:
            # Condtion 2
            db_name = "SwingData"
            conditionName = "Champions Swing" # change name Here
            CONDITION2 = {"scan_clause": "( {cash} ( ( {cash} ( ( {57960} ( ( {cash} ( latest cci( 20 ) >= 0 and weekly cci( 20 ) >= -150 and latest rsi( 14 ) > 30 and weekly rsi( 14 ) >= 45 and monthly rsi( 14 ) >= 50 and market cap > 250 and latest obv >= [0] 4 hour obv and latest macd line( 13 , 8 , 5 ) >= [0] 4 hour macd line( 13 , 8 , 5 ) and weekly obv >= 1 week ago obv and latest avg true range( 14 ) >= [0] 4 hour avg true range( 14 ) and weekly avg true range( 14 ) >= 1 week ago avg true range( 14 ) and earning per share[eps] > prev year eps ) ) ) ) ) ) ) )"}
            row_to_start ='F3'
            row_to_clean = "F3:I"
            conditionNameLocation = "E4"
            # chartinkLogicBankend(condition=CONDITION2,row_to_start=row_to_start,row_to_clean= row_to_clean,sheetname='Hello World',conditionName=conditionName,conditionNameLocation=conditionNameLocation)
            
            chartinkLogicBankend(condition=CONDITION2,conditionName=conditionName,db_name=db_name)
        except Exception as e:
            print(e)
        # Condtion 3        
        try:
            # condition 3
            db_name = "PositionalData"
            conditionName = "Champions Positional"
            CONDITION3 = {"scan_clause": "( {cash} ( ( {cash} ( ( {cash} ( ( {cash} ( ( {cash} ( weekly cci( 20 ) >= -100 and monthly cci( 20 ) >= 0 and weekly rsi( 14 ) >= 40 and monthly rsi( 14 ) >= 50 and market cap > 250 and weekly obv >= 1 week ago obv and weekly avg true range( 14 ) >= 1 week ago avg true range( 14 ) and weekly rsi( 14 ) >= 1 week ago rsi( 14 ) and monthly obv >= 1 week ago obv and monthly avg true range( 14 ) >= 1 week ago avg true range( 14 ) and ttm eps > prev year eps and yearly return on capital employed percentage >= 20 and yearly debt equity ratio <= 1 and yearly operating profit margin percentage >= 15 ) ) ) ) ) ) ) ) ) )"}
            row_to_start ='k3'
            row_to_clean = "k3:N"
            conditionNameLocation = "I4"
            # chartinkLogicBankend(condition=CONDITION3,row_to_start=row_to_start,row_to_clean= row_to_clean,sheetname='Hello World',conditionName=conditionName,conditionNameLocation=conditionNameLocation)
            chartinkLogicBankend(condition=CONDITION3, conditionName=conditionName,db_name=db_name)
        except Exception as e:
            print(e)
        # Condtion 4    
        try:
            # condition 4
            db_name = "ReversalData"
            conditionName = "Champions Reversal Stocks"
            CONDITION4 ={"scan_clause": "( {cash} ( 1 day ago cci( 20 ) <= -100 and latest cci( 20 ) >= 1 day ago cci( 20 ) and market cap >= 250 and latest close >= 1 day ago close and latest macd line( 26 , 12 , 9 ) >= [0] 4 hour macd line( 26 , 12 , 9 ) and latest obv >= 1 day ago obv and latest rsi( 14 ) >= 1 day ago rsi( 14 ) and latest adx di negative( 14 ) <= 1 day ago adx di negative( 14 ) and latest accdist  >= 1 day ago accdist  ) )"}
            # {"scan_clause":"( {cash} ( 1 day ago cci( 20 ) <= -100 and latest cci( 20 ) >= 1 day ago cci( 20 ) and market cap >= 250 and latest close >= 1 day ago close and latest macd line( 26 , 12 , 9 ) >= [0] 4 hour macd line( 26 , 12 , 9 ) and latest obv >= 1 day ago obv ) )"}
            # CONDITION4 = {"scan_clause": "( {cash} ( 1 day ago cci( 20 ) <= -100 and latest cci( 20 ) >= 1 day ago cci( 20 ) and market cap >= 250 ) )"}
            row_to_start ='P3'
            row_to_clean = "P3:S"
            conditionNameLocation = "M4"
            # chartinkLogicBankend(condition=CONDITION4,row_to_start=row_to_start,row_to_clean= row_to_clean,sheetname='Hello World',conditionName=conditionName,conditionNameLocation=conditionNameLocation)
            # print(conditionName)
            chartinkLogicBankend(condition=CONDITION4, conditionName=conditionName,db_name=db_name)
        except Exception as e:
            print(e) 
        # Condtion 5   
        try:
            # condition 5
            
            db_name = "OverBroughtData"
            conditionName = "Champions Over Brought"
            CONDITION5 = {"scan_clause": "( {33489} ( latest cci( 20 ) <= 1 day ago cci( 20 ) and latest obv < 1 day ago obv and latest macd line( 26 , 12 , 9 ) < 1 day ago macd line( 26 , 12 , 9 ) and weekly obv < 1 week ago obv and monthly obv < 1 month ago obv and weekly cci( 20 ) < 1 week ago cci( 20 ) and monthly cci( 20 ) < 1 month ago cci( 20 ) and [0] 15 minute close < 1 day ago close ) )"}
            # {"scan_clause": "( {33489} ( latest cci( 20 ) <= 1 day ago cci( 20 ) and latest obv < 1 day ago obv and latest macd line( 26 , 12 , 9 ) < 1 day ago macd line( 26 , 12 , 9 ) and weekly obv < 1 week ago obv and monthly obv < 1 month ago obv and weekly cci( 20 ) < 1 week ago cci( 20 ) and monthly cci( 20 ) < 1 month ago cci( 20 ) and [0] 30 minute close < 1 day ago close ) )"}
           
          
            row_to_start ='U3'
            row_to_clean = "U3:X"
            conditionNameLocation = "Q4"
            # chartinkLogicBankend(condition=CONDITION5,row_to_start=row_to_start,row_to_clean= row_to_clean,sheetname='Hello World',conditionName=conditionName,conditionNameLocation=conditionNameLocation)
            chartinkLogicBankend(condition=CONDITION5, conditionName=conditionName,db_name=db_name)
        except Exception as e:
            print(e)
        # Condtion 6  
        try:
            # condition 6
            # conditionName = "MOMENTUM BUY"  - to be change on 20.3.2024
            db_name = "Condition6"
            conditionName = "Champions Condition 6"
            CONDITION6 = {"scan_clause": "( {cash} ( ( {cash} ( ( {57960} ( ( {cash} ( latest cci( 20 ) >= 0 and weekly cci( 20 ) >= -150 and latest rsi( 14 ) > 30 and weekly rsi( 14 ) >= 45 and monthly rsi( 14 ) >= 50 and market cap > 250 and latest obv >= [0] 4 hour obv and latest macd line( 13 , 8 , 5 ) >= [0] 4 hour macd line( 13 , 8 , 5 ) and weekly obv >= 1 week ago obv and latest avg true range( 14 ) >= [0] 4 hour avg true range( 14 ) and weekly avg true range( 14 ) >= 1 week ago avg true range( 14 ) and monthly obv >= 1 month ago obv and monthly cci( 20 ) >= 1 month ago cci( 20 ) ) ) ) ) ) ) ) )"}
            row_to_start ='Z3'
            row_to_clean = "Z3:AC"
            conditionNameLocation = "U4"
            chartinkLogicBankend(condition=CONDITION6, conditionName=conditionName,db_name=db_name)
        except Exception as e:
            print(e)
        # Condtion 7    - Stopped by User - to be change on 20.3.2024
        # try:
        #     # condition 
        #     conditionName = "Monthly>60 Weekly>60 Daily 40-45"
        #     CONDITION7 = {"scan_clause": "( {57960} ( monthly rsi( 14 ) >= 60 and weekly rsi( 14 ) >= 60 and latest rsi( 14 ) >= 40 and latest rsi( 14 ) <= 45 ) )"}
        #     row_to_start ='AE3'
        #     row_to_clean = "AE3:AH"
        #     conditionNameLocation = "Y4"
        #     chartinkLogicBankend(condition=CONDITION7,row_to_start=row_to_start,row_to_clean= row_to_clean,sheetname='Hello World',conditionName=conditionName,conditionNameLocation=conditionNameLocation)
        # except Exception as e:
        #     print(e)
        # # # Condtion 8    - Stopped by User
        # try:
        #     # condition 8
        #     conditionName = "NIFTY 50"
        #     CONDITION8 = {"scan_clause": "( {33492} ( latest volume > 1 ) )"}
        #     row_to_start ='AJ3'
        #     row_to_clean = "AJ3:AM"
        #     conditionNameLocation = "AN4"
        #     # chartinkLogicBankend(condition=CONDITION8,row_to_start=row_to_start,row_to_clean= row_to_clean,sheetname='Hello World',conditionName=conditionName,conditionNameLocation=conditionNameLocation)
        #     chartinkLogicBankend(condition=CONDITION8)
        # except Exception as e:
        #     print(e)
        # # print(market)    
        # if(market == 'Closed' or market == "Close"):
        #     count +=1
        #     # print(f"Market is {count}<--->{market}")
        #     return {"Market Status" : f"{market}"}
        else:
            count +=1
            print(f"Market is {count}")
        time.sleep(10) # 300 seconds = 5 minutes
    # Sleep for 5 minutes``
        
    # time.sleep(120) # 300 seconds = 5 minutes
