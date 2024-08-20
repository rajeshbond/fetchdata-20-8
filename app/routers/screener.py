
from fastapi import HTTPException, APIRouter , BackgroundTasks
from ..functions.chartink import trasferDataToGoogleSheet

router = APIRouter(
    prefix= '/screener',
     tags=["Screener"]
)

@router.get("/api/screenerfetch")
def screenerfetch(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(trasferDataToGoogleSheet)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "code start Running"}


# @router.get("/api/nsefetch")
# async  def nsefetch():
#     try:
#         nse_data()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return {"message": "code start Running"}
