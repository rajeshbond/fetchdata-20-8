from fastapi import HTTPException
import pandas as pd
import datetime,os
import pytz
from ..database import get_db
from sqlalchemy import text, column
from sqlalchemy.sql import select
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from .comp import compare_csv_files
from .addfunda import piotista

FREQUENCY_DAY = 30 # 5 days FREQUENCY 

def get_last_n_working_days(n, start_date):
    # Convert start_date from string to datetime
    start_date = pd.to_datetime(start_date)

    days = []
    day_offset = 1  # Start with the previous day

    while len(days) < n:
        previous_day = start_date - pd.Timedelta(days=day_offset)
        if previous_day.weekday() < 5:  # Monday to Friday are working days
            days.append(previous_day)
        day_offset += 1
    return days



def frequency(data, conditionName):
    db = next(get_db())
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'], format="%Y-%m-%d")
    # data.to_csv(f'data_{conditionName}.csv', index=False)


    today = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).date()
    # print(f"Today's date: {today}")
    
    # Get last 5 working days
    last_5_working_days = get_last_n_working_days(FREQUENCY_DAY, today)
    last_5_working_days_str = [day.strftime('%d-%m-%Y') for day in last_5_working_days]
    last_5_working_days_str.append(today.strftime('%d-%m-%Y'))

    filtered_data = data[data['date'].dt.strftime('%d-%m-%Y').isin(last_5_working_days_str)]
    
    # Calculate frequency based on 'nsecode'to
    frequency = filtered_data['nsecode'].value_counts().reset_index()
    frequency.columns = ['nsecode', 'count']
    
    # Read and filter the additional CSV file
    chart_can = pd.read_csv(f'mid/{conditionName}.csv')
    filtered_chart_can = chart_can[chart_can['nsecode'].isin(frequency['nsecode'])]
    
    # Merge the dataframes
    result = filtered_chart_can.merge(frequency, on='nsecode')

    # Calculate the frequency of each 'igroup_name'
    igroup_name_count = result['igroup_name'].value_counts().reset_index()
    igroup_name_count.columns = ['igroup_name', 'igroup_name_count']
    
    # Merge igroup_name_count with the result DataFrame
    result = result.merge(igroup_name_count, on='igroup_name')
    
    # Calculate the frequency of each 'nsecode' in the result DataFrame
    nsecode_count = result['nsecode'].value_counts().reset_index()
    nsecode_count.columns = ['nsecode', 'count']
    
    # Merge nsecode_count with the result DataFrame
    result = result.merge(nsecode_count, on='nsecode')
    result = result.drop(columns=['count_y'])
    result = result.rename(columns={'count_x': 'count'})
    result = result.rename(columns={'igroup_name_count': 'frequency'})
    result = result.rename(columns={'igroup_name': 'sector'})
    selected_columns = ['nsecode', 'per_chg','close','date', 'sector','count','frequency']

    result_list = result[selected_columns]
    # print(result_list)
    file_name = f'result/result_{conditionName}.csv'
    if os.path.exists(file_name):
        old_data = pd.read_csv(file_name)
    else:
        old_data = pd.DataFrame(columns=selected_columns)

    # old_data = pd.read_csv(f'result/result_{conditionName}.csv')
    old_data = old_data.drop(columns=['date'])
    new_data_with_date = result_list.drop(columns=['date'])
    # print("----------------old data -----------------")
    # print(old_data)
    # print("----------------new data -----------------")
    # print(new_data_with_date)
    comp_result = compare_csv_files(old_data , new_data_with_date)
    # print(f"********* Comparison sorted result --> {comp_result}<--****************")
    # Save the result to a CSV file
    directory = 'result'
    if comp_result != True:
        if not os.path.exists(directory):
            os.makedirs(directory)
        result.to_csv(f'result/result_{conditionName}.csv', index=False)
        piotista(conditionName)
        # result_list = result.to_dict(orient='records')
        # print(f"New data record result/result_{conditionName}.csv")
    # print(f"------------------{conditionName}---------------------------")
    # print(result_list)

    
    return
    