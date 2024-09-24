import requests
import pandas as pd

# URL for AMFI NAV data
url = "https://www.amfiindia.com/spages/NAVAll.txt"

# Fetch the data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the data to a file with the correct encoding
    with open('amfi_nav.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)

    # Read the data into a DataFrame
    data = pd.read_csv('amfi_nav.txt', sep=';', header=None)

    # Print the first few rows to understand the structure
    print(data.head())
    print("Number of columns:", data.shape[1])

    # Set column names (adjust based on the actual number of columns)
    if data.shape[1] == 7:  # Check if there are 7 columns
        data.columns = ['Scheme Code', 'ISIN Div Payout', 'ISIN Growth', 'ISIN Div Reinvestment', 'Scheme Name', 'Net Asset Value', 'Date']
    else:
        print("Expected 7 columns, but got:", data.shape[1])

    # Save the DataFrame to a CSV file
    data.to_csv('amfi_nav.csv', index=False, encoding='utf-8')

    print("Data saved to amfi_nav.csv")
else:
    print("Failed to fetch data:", response.status_code)
