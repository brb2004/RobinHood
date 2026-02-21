import requests
import config.config_vars as config

URL = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"

def load_nasdaq_companies():
    response = requests.get(URL)
    response.raise_for_status()

    lines = response.text.splitlines()

    connection = config.get_connection()
    cursor = connection.cursor()

    try:
        for line in lines[1:-1]:
            parts = line.split("|")

            if len(parts) < 2:
                continue

            symbol = parts[0]
            name = parts[1]

            cursor.execute(""" INSERT IGNORE INTO companies (symbol, company_name, exchange)VALUES (%s, %s, 'NASDAQ') """, (symbol, name))

        connection.commit()
        print("NASDAQ companies loaded.")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_nasdaq_companies()