import requests
import json

# Define the URL
url = "https://www.mcxindia.com/BackPage.aspx/GetTicker"
# url = "https://www.mcxindia.com/backpage.aspx/GetMCXIComdexIndicesDetails"

# Define headers based on your provided request
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json; charset=UTF-8",
    "Cookie": "ASP.NET_SessionId=tf5lsipa5hau4tms0pr2druw; _gid=GA1.2.1622783788.1727249918; device-source=https://www.mcxindia.com/; device-referrer=; _gat_gtag_UA_121835541_1=1; _ga=GA1.1.1737698067.1724001452; _ga_8BQ43G0902=GS1.1.1727249917.3.1.1727250306.0.0.0",
    "Host": "www.mcxindia.com",
    "Origin": "https://www.mcxindia.com",
    "Referer": "https://www.mcxindia.com/",
    "Sec-CH-UA": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "Sec-CH-UA-Mobile": "?1",
    "Sec-CH-UA-Platform": '"Android"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# The data sent with the POST request (empty payload)
data = "{}"

# Make the POST request
response = requests.post(url, headers=headers, data=data)

# Directly decode the JSON response
json_data = response.json()

# Print the output in a readable format
print(json.dumps(json_data, indent=4))
