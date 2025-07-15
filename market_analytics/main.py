from get_market_tickets import *
from batching_dataset import batch_json_batches
from Niflheim_connector import *
import concurrent.futures

print("AAAAAAAAAAAAAAAAAAAAaa")
tenebrae = load_csv("zegnautus_data.csv")

print(tenebrae[0])
def find_symbol_id(base_url, api_key, symbol):
    try:
        url = f"{base_url}/v1/symbols/search?prefix={symbol}"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers)

        #print(response.status_code)

        if response.status_code == 200:
            data = response.json()
            if data.get("symbols"):
                return (symbol, data["symbols"][0]["symbolId"])
    except Exception as e:
        
        print(f"Error processing {symbol}: {e} ; ")
     
    return None

def fetch_all_ids_parallel(tenebrae, base_url, api_key, max_workers=10):
    symbol_ids = []
    counter = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_symbol = {
            executor.submit(find_symbol_id, base_url, api_key, entry['symbol']): entry['symbol']
            for entry in tenebrae
        }

        for future in concurrent.futures.as_completed(future_to_symbol):
            result = future.result()
            counter += 1
            print(counter)
            if result is not None:
                symbol_ids.append(result[1])

    return symbol_ids

#symbol_ids = fetch_all_ids_parallel(tenebrae, "https://api06.iq.questrade.com", 'SfEM6CrJtY-MapKLETAcVv1qBlzw-6IA0')


symbol_ids = []
counter = 0
for i in range(len(tenebrae)):
    current_id = find_symbol_id("https://api06.iq.questrade.com", 'SfEM6CrJtY-MapKLETAcVv1qBlzw-6IA0', tenebrae[i]['symbol'])
    if current_id != None:  
        print(current_id)
        
        symbol_ids.append(current_id[1])
    counter+=1
    print(counter)

print(symbol_ids)


with open("symbol_ids.json", "w") as f:
    json.dump(symbol_ids, f)


batch_json_batches("symbol_ids.json","niflheim_production_energy_175.json",175)

print("Saved symbol_ids.json")