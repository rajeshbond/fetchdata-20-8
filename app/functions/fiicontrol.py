import requests
from bs4 import BeautifulSoup
import pandas as pd
from functools import lru_cache

# Define the main function with caching
@lru_cache(maxsize=10)
def dataFiiDiiActivity():
    # URL of the website
    url = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"

    # Send an HTTP GET request to the website
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    # print(f"HTTP Status Code: {response.status_code}")

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the relevant table data
        table = soup.find('div', {'class': 'fifi_tblbrd'})

        data = []
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 7:
                    data.append({
                        'Date': cols[0].text.strip(),
                        'FII Buy Value': cols[1].text.strip(),
                        'FII Sell Value': cols[2].text.strip(),
                        'FII Net Value': cols[3].text.strip(),
                        'DII Buy Value': cols[4].text.strip(),
                        'DII Sell Value': cols[5].text.strip(),
                        'DII Net Value': cols[6].text.strip()
                    })

        # Clean and process the data
        # data_cleaning(data)
        # print(cleaned_data)
        return data
    else:
        print("Failed to fetch the page.")
        return []


def data_cleaning(data):
    df = pd.DataFrame(data)
    print("---------------------------------------------------------")
    print(df)
    # Clean 'Date' column: strip and remove newline characters
    df['Date'] = df['Date'].str.strip().replace('\n', '', regex=True)

    # Define the criteria to exclude rows where 'Date' is 'Month till date' or a specific unwanted date
    criteria = (df['Date'] != 'Month till date') & (df['Date'] != '24-Jul-2024')

    # Apply the criteria to filter the DataFrame
    filtered_df = df[criteria].copy()

    # Use regex to extract the relevant date
    filtered_df['Date'] = filtered_df['Date'].str.extract(r'(\d{2}-\w{3}-\d{4})')

    # Convert 'Date' column to datetime format
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d-%b-%Y', errors='coerce')

    # Drop rows where conversion failed (resulting in NaT)
    filtered_df = filtered_df.dropna(subset=['Date'])

    # Filter out weekends
    filtered_df = filtered_df[~filtered_df['Date'].dt.dayofweek.isin([5, 6])]

    # Sort the DataFrame by 'Date' in ascending order
    filtered_df = filtered_df.sort_values(by='Date', ascending=True)

    # Select the most recent 5 business days
    latest_five_business_days_df = filtered_df.tail(5).copy()

    # Format 'Date' to dd-mm-yyyy
    latest_five_business_days_df['Date'] = latest_five_business_days_df['Date'].dt.strftime('%d-%m-%Y')

    return latest_five_business_days_df.to_dict(orient='records')

def fetch_fii_dii_data_and_format():
    data = dataFiiDiiActivity()
    formatted_data = data_cleaning(data)
    print("---------------------------------------------------------")
    print(formatted_data)
    return formatted_data

# Call the function (uncomment to test)
# print(fetch_fii_dii_data_and_format())
