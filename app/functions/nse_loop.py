import logging
import time
from fastapi import HTTPException
from .new_nse import market_status_1, fetch_nifty_data_index, indexes_all
from .nse_func import board_meetings
from .stockedge import new_top_news

# Configure logging to write errors to a text file
logging.basicConfig(
    filename="error_log.txt",  # Log file path
    level=logging.ERROR,  # Log only errors and above
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format for log entries
)

def safe_execute(func, *args, **kwargs):
    """Helper to execute a function with error logging."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_message = f"Error in {func.__name__}: {str(e)}"
        logging.error(error_message)  # Log the error
        raise HTTPException(status_code=500, detail=error_message)

def start_loop():
    """Fetch market indices repeatedly when the market is open."""
    count = 0

    while True:
        market = safe_execute(market_status_1)
        time.sleep(10)  # Wait for 10 seconds before checking status again

        # if market.lower() in ["closed", "close"]:
        #     print("Market is closed. Exiting the program.")
        #     break

        print(f"----Count: {count + 1} {market}----")
        
        # Safely fetch NIFTY data and all indices
        safe_execute(fetch_nifty_data_index, 
                     "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK", 
                     "NIFTY BANK")
        safe_execute(fetch_nifty_data_index, 
                     "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050", 
                     "NIFTY 50")
        safe_execute(indexes_all)

        if market.lower() in ["closed", "close"]:
            print("Market is closed. Exiting the program.")
            break

        count += 1
        time.sleep(20)  # Wait 20 seconds before next iteration

    print("Exited the loop gracefully.")

def start_loop_news():
    """Fetch market news and board meetings repeatedly when the market is open."""
    count = 0

    while True:
        market = safe_execute(market_status_1)
        time.sleep(10)  # Wait for 10 seconds before checking status

        if market.lower() in ["closed", "close"]:
            print("Market is closed. Exiting the news fetch loop.")
            break

        print(f"----Count: {count + 1} {market}----")
        
        # Safely fetch news and board meetings
        safe_execute(new_top_news)
        safe_execute(board_meetings)

        count += 1
        time.sleep(3600)  # Wait for 1 hour before fetching again
        if market.lower() in ["closed", "close"]:
            print("Market is closed. Exiting the news fetch loop.")
            break

    print("Exited the news fetch loop gracefully.")




# Old verson code



# from .nse_data import getIndex , indexfetch, indexfetch_heat , market_status
# from .nse_func import current_ipo, board_meetings
# from .stockedge import new_top_news
# from fastapi import HTTPException
# import time

# def start_loop():
#    count = 0
#    flag = True
#    market=  market_status()
#    while flag:
#       try:
#          #  To fetch the NIFTY BANK index
#          getIndex("NIFTY BANK")  
#       except Exception as e:
#          raise HTTPException(status_code=500, detail=str(e))
#       try:
#          #  To fetch the NIFTY 50 index
#          getIndex("NIFTY 50")
#       except Exception as e:
#          raise HTTPException(status_code=500, detail=str(e))
#       try:
#          #  To fetch the all index
#          indexfetch()
#       except Exception as e:
#          raise HTTPException(status_code=500, detail=str(e))
#       try:
#          #  To fetch the all index_for heatmap
#          indexfetch_heat()
#       except Exception as e:
#          raise HTTPException(status_code=500, detail=str(e))
#       try:
#          if (market == "Closed" or market== "Close"):
#             print("Market is closed. Hence exiting the program.")
#             flag = False
#          else:
#             count += 1
#             print(f"----Count: {count} {market}---")
#             time.sleep(20)    # to fetch it after every 20 seconds When the market is open
#             continue
#       except Exception as e:
#          raise HTTPException(status_code=500, detail=str(e))
      

# def start_loop_news():
#    count = 0
#    market=  market_status()
#    while True:
#       try:
#          new_top_news()
#       except Exception as e:
#          raise HTTPException(status_code=500, detail=str(e))
#       try:
#          board_meetings()
#       except Exception as e:
#          raise HTTPException(status_code=500, detail=str(e))
      
#       try:
#          if (market == "Closed" or market== "Close"):
#             print("Market is closed. Hence exiting the program.")
#             break
#          else:
#             count += 1
#             print(f"----Count: {count} {market}---")
#             time.sleep(45)
#             continue
#       except Exception as e:
#          raise HTTPException(status_code=500, detail=str(e))