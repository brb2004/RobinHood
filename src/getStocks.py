import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import pymysql
from config_vars import connection, cursor

load_dotenv()

API_KEY = os.getenv("POLYGON_API_KEY")

def get_symbols(limit=10):
    url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&limit={limit}&apiKey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    symbols = []

    for ticker in data.get("results", []):
        symbol = ticker.get("ticker")
        company_name = ticker.get("name")

        if symbol and company_name:
            symbols.append((symbol, company_name))

    return symbols


def get_stock_price(symbol):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    results = data.get("results")

    if results:
        close_price = results[0]["c"]
        open_price = results[0]["o"]

        percent_change = ((close_price - open_price) / open_price) * 100

        timestamp = results[0]["t"]
        date = datetime.fromtimestamp(timestamp / 1000).date()

        return close_price, percent_change, date
    return None, None, None

def insert_stock(symbol, company_name, price, percent_change, date):
    try:
        cursor.execute(
            """
            INSERT INTO stocks (symbol, company_name, price, percent_change, date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (symbol, company_name, price, percent_change, date)
        )
        connection.commit()

    except pymysql.err.IntegrityError:
        # Duplicate symbol/date
        pass

    except Exception as e:
        print("Insert error:", e)

def main():

    symbols = get_symbols(limit=10)

    print(f"Found {len(symbols)} symbols")

    for symbol, company_name in symbols:

        print(f"Fetching {symbol}")

        price, percent_change, date = get_stock_price(symbol)
        if price and date:
            insert_stock(symbol, company_name, price, percent_change, date)

    print("Stock load complete")


if __name__ == "__main__":
    main()
