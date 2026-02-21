import requests
from src.config import config_vars as config
import time

BASE_URL = "https://api.polygon.io"


def get_symbols(limit=100):
    url = f"{BASE_URL}/v3/reference/tickers"

    params = {
        "market": "stocks",
        "exchange": "XNAS",
        "active": "true",
        "limit": limit,
        "apiKey": config.POLYGON_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return [ticker["ticker"] for ticker in data.get("results", [])]


def get_stock_price(symbol):
    url = f"{BASE_URL}/v2/aggs/ticker/{symbol}/prev"

    params = {
        "adjusted": "true",
        "apiKey": config.POLYGON_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error fetching {symbol}: {response.text}")
        return None

    data = response.json()

    if not data.get("results"):
        return None

    result = data["results"][0]

    price = result["c"]
    volume = result["v"]
    timestamp = result["t"]

    open_price = result["o"]
    percent_change = ((price - open_price) / open_price) * 100 if open_price else 0

    return price, percent_change, volume, timestamp


def insert_stock_price(symbol, price, percent_change, volume, timestamp):
    connection = config.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT IGNORE INTO companies (symbol) VALUES (%s)",
            (symbol,)
        )

        query = """INSERT INTO stock_prices (symbol, price, percent_change, volume, market_timestamp) VALUES (%s, %s, %s, %s, FROM_UNIXTIME(%s / 1000)) 
                ON DUPLICATE KEY UPDATE 
                price = VALUES(price),
                percent_change = VALUES(percent_change),
                volume = VALUES(volume)
                """

        cursor.execute(query, (symbol, price, percent_change, volume, timestamp))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def main():
    symbols = get_symbols(limit=100)

    print(f"Found {len(symbols)} symbols")

    for symbol in symbols:
        print(f"Fetching {symbol}")

        stock_data = get_stock_price(symbol)

        if not stock_data:
            continue

        price, percent_change, volume, timestamp = stock_data

        insert_stock_price(symbol, price, percent_change, volume, timestamp)

        time.sleep(12)  

    print("Stock data loaded successfully")


if __name__ == "__main__":
    main()