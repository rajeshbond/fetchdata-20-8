from fastapi import APIRouter, HTTPException, BackgroundTasks,status
from ..functions.nse_loop import start_loop, start_loop_news
from ..functions.nse_func import current_ipo, board_meetings,block_deals,bulk_deals
router = APIRouter(
    prefix= '/input_start',
     tags=["Input Record"]
)

@router.post("/api/inputrecord", status_code=status.HTTP_200_OK)
def screenerinput(background_tasks: BackgroundTasks):
  try:
    background_tasks.add_task(start_loop)
    return {"message": "Input Start"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.post("/api/ipo", status_code=status.HTTP_200_OK)
def fetchIPO():
  try:
    ipo_data = current_ipo()
    return {"message": ipo_data}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.post("/api/boardmeetings", status_code=status.HTTP_200_OK)
def boardMeetings():
  try:
    boardMeetings = board_meetings()
    return {"message": boardMeetings}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.post("/api/inputnews", status_code=status.HTTP_200_OK)
def screenerinput(background_tasks: BackgroundTasks):
  try:
    background_tasks.add_task(start_loop_news)
    return {"message": "Input Start"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/blockdeals", status_code=status.HTTP_200_OK)
def blockDeals():
  try:
    bulk_deals()
    return {"message": "Data Fetched"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.post("/api/dayblock", status_code=status.HTTP_200_OK) 
def dayBlock():
  try:
    block_deals()
    return {"message": "Data Fetched"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
