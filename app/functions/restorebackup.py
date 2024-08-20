from fastapi import Response, status, HTTPException, Depends, APIRouter
import pandas as pd
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session

def restorebackupfun():
  # db_name = ['IntradayData', 'OverBroughtData', 'PositionalData', 'ReversalData', 'SwingData']
  db_name = ['Condition6']
  try:
    print("restorebackupfun")
    for name in db_name:
      print(name)
      doRestore(name)
    return {"message": "success"}
  except Exception as e:
    return {"message": str(e)}

def doRestore(db_name):
    print(f"doRestore ---> {db_name}")
    try:
        db = next(get_db())
        model_mapping = {
            # "IntradayData": models.IntradayData,
            # "OverBroughtData": models.OverBroughtData,
            # "PositionalData": models.PositionalData,
            # "ReversalData": models.ReversalData,
            # "SwingData": models.SwingData,
            "Condition6": models.Condition6
        }

        # Get the appropriate model class
        model_class = model_mapping.get(db_name)
        print(f"model_class ---> {model_class}")
        if not model_class:
            print(f"No model mapping found for {db_name}")
            return

        # Read the CSV file
        data = pd.read_csv(f'download/{db_name}.csv')
        # data = pd.read_csv("download/ReversalData.csv")

        print(data)
        # Drop unnecessary columns
        filtered_data = data.drop(['id', 'create_at'], axis=1, errors='ignore')
        
        # Select specific columns
        selected_columns = ['nsecode', 'name', 'bsecode', 'per_chg', 'close', 'volume', 'date', 'time', 'igroup_name']
        final_data = filtered_data[selected_columns]
        print(final_data)
        # Insert data into the database
        db.bulk_insert_mappings(model_class, final_data.to_dict('records'))
        db.commit()
        print(f"Data successfully restored for {db_name}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))