import requests
import json
import time

from pathlib import Path
import csv

# Replace this with your actual access token and server
access_token = '2pA5WXpvo2EZNSTvZgaRpefY45MyvIht0'

server = 'https://api01.iq.questrade.com'

#access_server = 'https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token='

# Define the endpoint

def load_csv(filename):
    file = Path(__file__).parent / filename
    with file.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row]
    

tenebrae = load_csv("zegnautus_data.csv")
print(tenebrae[0])

#8049
#CJ = 5101915
initial_refresh_token = 'z6wj5wfpSjP-1qsjxzQjYMEnLwQqfpBU0'

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
    
#GET https://api01.iq.questrade.com/v1/symbols/search?prefix=BMO         look for a symbol by ticker, to retrieve its symbol id

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


'''current_symbol_id = find_symbol_id("https://api07.iq.questrade.com", '29rngV0uOJ5kz5i09Pex94sGIAMsCR4e0', tenebrae[0]['symbol'])
print(current_symbol_id)'''

new_refresh_token = 'hJKJsT_PJItpU0YOvx4ocwdghAdbma_L0'



#print('\n\n\n\n\n',find_stock_data("https://api07.iq.questrade.com", '29rngV0uOJ5kz5i09Pex94sGIAMsCR4e0', current_symbol_id[1]))

'''symbol_ids = []
counter = 0
for i in range(len(tenebrae)):
    current_id = find_symbol_id("https://api06.iq.questrade.com", '5et9kvRpOnnTxa4k491D9B0GyG68wRuX0', tenebrae[i]['symbol'])
    if current_id != None:
        
        symbol_ids.append(current_id[1])
    counter+=1
    print(counter)

print(symbol_ids)

with open("symbol_ids.json", "w") as f:
    json.dump(symbol_ids, f)

print("Saved symbol_ids.json")'''

'''i = 0
print(find_stock_id("https://api07.iq.questrade.com", '1iP-i3owqwbO_Wnni8hyPDN92_Rj0fup0', tenebrae[i]['symbol']))
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

     

url = f'{"https://api02.iq.questrade.com"}/v1/symbols?ids=37296,15987900,15310895,41664,1647794,36621,13689120,14308905,28791606,6462,30319645,31073,11593,14326,16073,20702195,32609028,22992154,52629133,2419327,11736542,1630021,15354154,35852972,15613,18065401,25829,10820435,34871423,28196,25051,4506918,2719218,19788839,2735405,19352199,1496794,2591025,27001178,36971,35892,36378,35258501,39690195,30489711,46178,20349846,29142531,39230534,3446900,19084,39465968,1247658'

headers = {
'Authorization': f'Bearer {'6N1xn-rEJAZqMlm36pzN7fETwR3MhMGV0'}'
}

response = requests.get(url, headers=headers)

# Print status and result
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2)) 