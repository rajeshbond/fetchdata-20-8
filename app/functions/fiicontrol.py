import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_fii_dii_data():
    url = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('div', {'class': 'fifi_tblbrd'})

    # Extract table data
    data = []
    if table:
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                data.append({
                    'Date': cols[0].text.strip(),
                    'FII Buy Value': cols[1].text.strip(),
                    'FII Sell Value': cols[2].text.strip(),
                    'FII Net Value': cols[3].text.strip(),
                    'DII Buy Value': cols[4].text.strip(),
                    'DII Sell Value': cols[5].text.strip(),
                    'DII Net Value': cols[6].text.strip()
                })

    return data

def format_data(data):
    
    formatted = "Category,Date,Buy Value,Sell Value,Net Value\n"
    for row in data:
        formatted += f"{row['Date']},{row['FII Buy Value']},{row['FII Sell Value']},{row['FII Net Value']},{row['DII Buy Value']},{row['DII Sell Value']},{row['DII Net Value']}\n"
    return formatted




def data_cleaning(data):
    df = pd.DataFrame(data)
    
    # Clean 'Date' column: strip and remove newline characters
    df['Date'] = df['Date'].str.strip().replace('\n', '', regex=True)

    # Define the criteria to exclude rows where 'Date' is 'Month till date' or '24-Jul-2024'
    criteria = (df['Date'] != 'Month till date') & (df['Date'] != '24-Jul-2024')

    # Apply the criteria to filter the DataFrame
    filtered_df = df[criteria].copy()  # Ensure we work on a copy to avoid SettingWithCopyWarning

    # Use regex to extract the relevant date
    filtered_df['Date'] = filtered_df['Date'].str.extract(r'(\d{2}-\w{3}-\d{4})')

    # Convert 'Date' column to datetime format
    try:
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d-%b-%Y', errors='coerce')
    except Exception as e:
        print(f"Date conversion error: {e}")
        return []

    # Check if any conversion failed
    if filtered_df['Date'].isna().all():
        print("All date conversions failed.")
        return []

    # Drop rows where conversion failed (resulting in NaT)
    filtered_df = filtered_df.dropna(subset=['Date'])

    # Check if there are any remaining dates after dropping NaT
    if filtered_df.empty:
        print("No valid dates remaining after dropping NaT.")
        return []

    # Filter out weekends
    try:
        filtered_df = filtered_df[~filtered_df['Date'].dt.dayofweek.isin([5, 6])]
    except Exception as e:
        print(f"Error filtering weekends: {e}")
        return []

    # Sort the DataFrame by 'Date' in ascending order
    filtered_df = filtered_df.sort_values(by='Date', ascending=True)

    # Select the most recent 5 business days
    latest_five_business_days_df = filtered_df.tail(5).copy()

    # Format 'Date' to dd-mm-yyyy
    try:
        latest_five_business_days_df['Date'] = latest_five_business_days_df['Date'].dt.strftime('%d-%m-%Y')
    except Exception as e:
        print(f"Error formatting dates: {e}")
        return []

    # Convert the resulting DataFrame to a list of dictionaries
    latest_five_business_days_data_as_list = latest_five_business_days_df.to_dict(orient='records')

    # Print the cleaned data
    # print("\nLatest Five Business Days Data in Ascending Order as List of Dictionaries:")
    print(latest_five_business_days_data_as_list)
    
    return latest_five_business_days_data_as_list




# def data_cleaning(data):
#   df = pd.DataFrame(data)
#   df['Date'] = df['Date'].str.strip().replace('\n', '', regex=True)

#   # Define the criteria to exclude rows where 'Date' is 'Month till date' or '24-Jul-2024'
#   criteria = (df['Date'] != 'Month till date') & (df['Date'] != '24-Jul-2024')

#   # Apply the criteria to filter the DataFrame
#   filtered_df = df[criteria]

#   # Use regex to extract the relevant date
#   filtered_df['Date'] = filtered_df['Date'].str.extract(r'(\d{2}-\w{3}-\d{4})')

#   # Convert 'Date' column to datetime format
#   filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d-%b-%Y')

#   # Filter out weekends
#   filtered_df = filtered_df[~filtered_df['Date'].dt.dayofweek.isin([5, 6])]

#   # Sort the DataFrame by 'Date' in ascending order
#   filtered_df = filtered_df.sort_values(by='Date', ascending=True)

#   # Select the most recent 5 business days (which are now the earliest 5 after sorting)
#   latest_five_business_days_df = filtered_df.tail(5)

#   # Format 'Date' to dd-mm-yyyy
#   latest_five_business_days_df['Date'] = latest_five_business_days_df['Date'].dt.strftime('%d-%m-%Y')

#   # Convert the resulting DataFrame to a list of dictionaries
#   latest_five_business_days_data_as_list = latest_five_business_days_df.to_dict(orient='records')

#   # Print the cleaned data
#   print("\nLatest Five Business Days Data in Ascending Order as List of Dictionaries:")
#   # print(latest_five_business_days_data_as_list)
#   return latest_five_business_days_data_as_list

    

def fetch_fii_dii_data_and_format():
    data = fetch_fii_dii_data()
    final_data = data_cleaning(data)
    # print("---------------------------------------------------------")
    # print(final_data)
    return final_data

# fetch_fii_dii_data_and_format()
