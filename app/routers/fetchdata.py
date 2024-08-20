import pandas as pd
from fastapi import Response, status, HTTPException, Depends, APIRouter , BackgroundTasks
from sqlalchemy.orm import Session
from ..import schemas,models
from ..database import get_db
from typing import List
from sqlalchemy import desc , text
from ..functions.nse_data import market_status


router = APIRouter(
    prefix= '/fetchdata',
     tags=["Screener Data"]
)


@router.post("/api/fetchdata", status_code=status.HTTP_200_OK,response_model=List[schemas.DataFetchout])
def fetchdata(condition: schemas.DataFetch):
    try:
        # print(condition.conditionName)
        file_name = f"result1/result_{condition.conditionName}.csv"
        # print(file_name)
        status = market_status()
        # if(status == 'Closed' or status == "Close"):
        #     return {"message": "Market Closed"}
        data = pd.read_csv(file_name)
        result =  data.to_dict(orient='records')
        # print(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/api/fetchfrequency", status_code=status.HTTP_200_OK)
def fetchfrequency(freq_details: schemas.frequencyFetchIn, db: Session = Depends(get_db)):
    # print(f"------------------->{freq_details}")
    try:
        # Construct the query with a dynamic table name
        query = text(f"""
        SELECT * 
        FROM public."{freq_details.tableName}"
        WHERE nsecode = :nsecode
        ORDER BY date DESC
        LIMIT :count;
        """)

        # Execute the query and fetch data into a DataFrame
        df = pd.read_sql_query(query, db.bind, params={"nsecode": freq_details.nsecode, "count": freq_details.count})
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%m-%Y')
        redefine = df.drop(['id','name','bsecode','volume','time','per_chg','igroup_name','create_at'], axis=1)
       # Convert the DataFrame to a dictionary
        # print(redefine)
        data = redefine.to_dict(orient="records")
        
        # Convert the DataFrame to a dictionary
   

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"data": data}
