import os
import pandas as pd

def piotista(conditionName):
    try:
        print(f"conditonName --> {conditionName}")
        file_name = f'result/result_{conditionName}.csv'
        result = pd.read_csv(file_name)
        pioFile = pd.read_csv('funda/screener_data_ot.csv')
        
        # Merge the data frames
        result = pd.merge(result, pioFile[['nsecode', 'Piotrski']], on='nsecode', how='left')
        
        # Convert Piotrski column to integers
        result['Piotrski'] = result['Piotrski'].fillna(2).astype(int)
        directory = 'result1'
        if not os.path.exists(directory):
            os.makedirs(directory)
        result.to_csv(f'result1/result_{conditionName}.csv', index=False)
        result_list = result.to_dict(orient='records')
        
        print(result)
    except Exception as e:
        print(f"piotista error: {e}")

