import requests
import csv




  
# Replace with your actual FMP API key
API_KEY = "JjwRNLq3SbyLDu3liyptodgovK0h8lMi"


URL = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}"

# Exchange codes for US and Canada
EXCHANGES = ["NASDAQ", "New York Stock Exchange", "Other OTC", "Toronto Stock Exchange", "Toronto Stock Exchange Ventures"]

def fix_ticker_format(ticker: str) -> str:
    """
    Convert tickers with hyphens like 'DHT-UN.TO' to dot format 'DHT.UN.TO'
    """
    if '-' in ticker:
        parts = ticker.split('-')
        if len(parts) == 2:
            base, suffix = parts
            if '.' in suffix:
                subparts = suffix.split('.')
                return f"{base}.{subparts[0]}.{subparts[1]}"
            else:
                return f"{base}.{suffix}"
    return ticker

def fetch_us_canada_tickers():
    print("Fetching stock list from FMP...")
    response = requests.get(URL)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    all_stocks = response.json()
    print(f"Total stocks received: {len(all_stocks)}")

    

    us_canada_stocks = [
        stock for stock in all_stocks if stock.get("exchange") in EXCHANGES 
        
    ]

    #print(all_stocks[2709].get("symbol"))

    print(f"Filtered US/Canada tickers: {len(us_canada_stocks)}")

    # Fix ticker format
    for stock in us_canada_stocks:
        stock["symbol"] = fix_ticker_format(stock["symbol"])

    return us_canada_stocks

def save_tickers_to_csv(ticker_list, filename="gralea_data.csv"):
    with open(filename, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["symbol", "name", "exchange", "currency"])
        writer.writeheader()
        for stock in ticker_list:
            writer.writerow({
                "symbol": stock.get("symbol"),
                "name": stock.get("name"),
                "exchange": stock.get("exchange"),
                "currency": stock.get("currency")
            })
    print(f"Saved tickers to {filename}")

# Run it
tickers = fetch_us_canada_tickers()
save_tickers_to_csv(tickers)