import requests
import json
import time

from pathlib import Path
import csv

# Replace this with your actual access token and server
access_token = ''

server = 'https://api01.iq.questrade.com'

#access_server = 'https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token='

# Define the endpoint

def load_csv(filename):
    file = Path(__file__).parent / filename
    with file.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row]
    



#8049
#CJ = 5101915
initial_refresh_token = ''

def wait_precise(seconds):
    start = time.perf_counter()
    while time.perf_counter() - start < seconds:
        pass


def refresh_questrade_token(refresh_token: str) -> tuple[str, str]:
    base_url = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=" 
    
    response = requests.get(base_url+refresh_token)

    if response.status_code == 200:
        data = response.json()
        return data["access_token"], data["refresh_token"], data["api_server"]
    else:
        raise RuntimeError(f"Failed to refresh token: {response.status_code} - {response.text}")
    

def find_symbol_id(server,access_token,symbol) -> int:


    
    url = f'{server}/v1/symbols/search?prefix={symbol}'
    
    headers = {
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    data  = response.json()    
    
    #print(data)
    if len(data["symbols"]) == 0:
        return None
    return (response.status_code,data["symbols"][0]["symbolId"]) 



def find_stock_data(server,access_token,id):
    url = f'{server}/v1/symbols/{id}'

    headers = {
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    return response.json()
    

def find_stock_id(server, access_token, current_symbol):


    current_symbol_id = find_symbol_id(server, access_token, current_symbol)
    print(current_symbol_id)

    stock_data = find_stock_data(server, access_token, current_symbol_id[1])
    return stock_data['symbols'][0]



new_refresh_token = ''




'''symbol_ids = []
counter = 0
for i in range(len(tenebrae)):
    current_id = find_symbol_id("https://api06.iq.questrade.com", '', tenebrae[i]['symbol'])
    if current_id != None:
        
        symbol_ids.append(current_id[1])
    counter+=1
    print(counter)

print(symbol_ids)

with open("symbol_ids.json", "w") as f:
    json.dump(symbol_ids, f)

print("Saved symbol_ids.json")'''

'''i = 0
print(find_stock_id("https://api07.iq.questrade.com", '', tenebrae[i]['symbol']))
'''
'''while True:

    url = f'{server}/v1/symbols/5101915'

    headers = {
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    # Print status and result
    print("Status Code:", response.status_code)
    #print("Response:", json.dumps(response.json(), indent=2)) 

    if response.status_code == 401:  # Unauthorized
        print("Access token expired, refreshing...")
        access_token, new_refresh_token, server = refresh_questrade_token(new_refresh_token)
        initial_refresh_token = new_refresh_token
        print("New access token: ", access_token, "New refresh token: ", new_refresh_token, "New server: ", server)


    wait_precise(100)'''

     

url = f'{"https://api02.iq.questrade.com"}/v1/symbols?ids=54297541'

url2= 'https://api06.iq.questrade.com/v1/symbols/search?prefix=QQQY.TO'
headers = {
'Authorization': f'Bearer {''} ',
}

response = requests.get(url2, headers=headers)

# Print status and result
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2)) 

