from .nse_data import getIndex , indexfetch, indexfetch_heat , market_status
from .nse_func import current_ipo, board_meetings
from .stockedge import new_top_news
from fastapi import HTTPException
import time

def start_loop():
   count = 0
   market=  market_status()
   while True:
      try:
         #  To fetch the NIFTY BANK index
         getIndex("NIFTY BANK")  
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
      try:
         #  To fetch the NIFTY 50 index
         getIndex("NIFTY 50")
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
      try:
         #  To fetch the all index
         indexfetch()
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
      try:
         #  To fetch the all index_for heatmap
         indexfetch_heat()
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
      try:
         if (market == "Closed" or market== "Close"):
            print("Market is closed. Hence exiting the program.")
            break
         else:
            count += 1
            print(f"----Count: {count} {market}---")
            time.sleep(20)    # to fetch it after every 20 seconds When the market is open
            continue
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
      

def start_loop_news():
   count = 0
   market=  market_status()
   while True:
      try:
         new_top_news()
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
      try:
         board_meetings()
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
      
      try:
         if (market == "Closed" or market== "Close"):
            print("Market is closed. Hence exiting the program.")
            break
         else:
            count += 1
            print(f"----Count: {count} {market}---")
            time.sleep(7200)
            continue
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))