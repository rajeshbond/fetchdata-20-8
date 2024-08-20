from sqlalchemy.orm import Session
from ..functions import restorebackup
from ..database import get_db
from .. import models
from fastapi import Response, status, HTTPException, Depends, APIRouter
import pandas as pd
import requests,json, datetime

router = APIRouter(
    prefix= '/symbols',
     tags=["Symbols"]
)

# symbols.py

@router.post("/api/daily")
def enter_symbols(db: Session = Depends(get_db)):
    try:
        file_to_open = "app/source/combined_equity.csv"
        # Step 1: Read the file from combined_equity.csv
        data_csv = pd.read_csv(file_to_open)

        # Step 2: Fill null values with default values
        data_csv['nsecode'] = data_csv['nsecode'].fillna('NA')  # Replace NaN in nsecode with 'NA'
        data_csv['bsecode'] = data_csv['bsecode'].fillna(0)     # Replace NaN in bsecode with 0

        # Define the valid columns present in the Symbol model
        valid_columns = ['bsecode', 'nsecode', 'name_of_the_company', 'status', 'face_value', 'isin_number', 'igroup_name']

        # Ensure only the valid columns are in the DataFrame
        data_csv = data_csv[valid_columns]

        # Create Symbol objects
        symbol_objects = data_csv.apply(lambda row: models.Symbol(**row.to_dict()), axis=1).tolist()
        print(symbol_objects)

        # Step 3: Check if the Symbols table is empty
        symbolList = db.query(models.Symbol).all()
        if not symbolList:
            print("empty")
            # Step 4: Add the data_csv to Symbols in bulk
            data_dict = data_csv.to_dict(orient='records')
            db.bulk_insert_mappings(models.Symbol, data_dict)
            db.commit()
            return {"message": "Symbols added successfully"}
        else:
            existing_symbols_df = pd.DataFrame([symbol.__dict__ for symbol in symbolList])
            new_entries_df = data_csv[~data_csv[['nsecode', 'bsecode']].apply(tuple, 1).isin(existing_symbols_df[['nsecode', 'bsecode']].apply(tuple, 1))]
            if not new_entries_df.empty:
                # Convert new entries to list of dictionaries
                new_entries = new_entries_df.to_dict(orient='records')
                # Add new entries to the database
                db.bulk_insert_mappings(models.Symbol, new_entries)
                db.commit()
                return {"message": f"{len(new_entries)} new symbols added successfully"}
            else:
                return {"message": "No new symbols to add"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))    
    
@router.delete("/day-symbols/")
def delete_symbols(db: Session = Depends(get_db)):
    try:
        db.query(models.DaySymbol).delete()
        db.query(models.DayNSEData).delete()
        db.commit()
        return {"message": "data deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/restorebackup")
def restore_backup(db: Session = Depends(get_db)):
    try:
        restorebackup.restorebackupfun()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))