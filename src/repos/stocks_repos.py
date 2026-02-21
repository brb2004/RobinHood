from src.config.config_vars import get_connection


class StocksRepo:

    def get_custom_stocks(self, stocks, items=None):
        if not stocks:
            return None

        connection = get_connection()
        cursor = connection.cursor()

        try:
            placeholders = ", ".join(["%s"] * len(stocks))
            base_query = f"""
                SELECT sp.symbol,
                    sp.price,
                    sp.percent_change,
                    sp.volume,
                    sp.market_timestamp
                FROM stock_prices sp
                WHERE sp.symbol IN ({placeholders})
                ORDER BY sp.market_timestamp DESC
            """
            params = list(stocks)
            cursor.execute(base_query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()


repo = StocksRepo()

result = repo.get_custom_stocks(
    stocks=["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"],
    items=["earnings", "dividend"]
)

print(result)