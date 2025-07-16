import requests

API_KEY = ""
URL = f"https://financialmodelingprep.com/api/v3/exchanges-list?apikey={API_KEY}"

# Define standard exchange names for US/Ca
# Define standard exchange names for US/Ca
EXPECTED = {
    "NASDAQ", "New York Stock Exchange",
    "AMEX", "Toronto Stock Exchange",
    "Toronto Stock Exchange Ventures", "Cboe Canada"
}

def find_unusual_exchanges():
    resp = requests.get(URL)
    resp.raise_for_status()
    exchanges = resp.json()

    unusual = []
    for ex in exchanges:
        print(ex)
    return sorted(set(unusual))

def print_unusual_exchanges():
    weird = find_unusual_exchanges()
    print("Verbose or non-standard exchange names for known US/CA codes:")
    for name in weird:
        print("•", name)

print_unusual_exchanges()