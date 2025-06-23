import requests
import csv




  
# Replace with your actual FMP API key
API_KEY = "JjwRNLq3SbyLDu3liyptodgovK0h8lMi"

# FMP endpoint for all tickers
URL = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}"

# Exchange codes for US and Canada
EXCHANGES = ["NASDAQ", "New York Stock Exchange", "Other OTC","Toronto Stock Exchange", "Toronto Stock Exchange Ventures"]


def fetch_us_canada_tickers():
    print("Fetching stock list from FMP...")
    response = requests.get(URL)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    all_stocks = response.json()
    print(f"Total stocks received: {len(all_stocks)}")

    us_canada_stocks = [
        stock for stock in all_stocks
        if stock.get("exchange") in EXCHANGES
    ]

    print(f"Filtered US/Canada tickers: {len(us_canada_stocks)}")

    return us_canada_stocks

def save_tickers_to_csv(ticker_list, filename="zegnautus_data.csv"):
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
 


tickers = fetch_us_canada_tickers()
save_tickers_to_csv(tickers)