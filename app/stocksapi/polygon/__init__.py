"""Polygon API Module"""

import os
from datetime import date, datetime
from pprint import pformat

from dotenv import load_dotenv
from polygon import RESTClient
from polygon.rest.models.aggs import DailyOpenCloseAgg, PreviousCloseAgg
from urllib3.response import HTTPResponse

load_dotenv()  # take environment variables from .env.
client = RESTClient(api_key=os.environ.get("POLYGONIO_API_KEY"))

APPLE_TICKER = "AAPL"


class PolygonAPIException(Exception):
    """Polygon API Exception"""


class ServiceLayer:
    """Service layer for Polygon API"""

    def __init__(self, rest_client: RESTClient = client):
        """Init function"""
        # TODO Inject dependency `client`
        self.client = rest_client

    def _get_previous_close(self, ticker: str) -> dict:
        """Get the previous day's open, high, low, and close (OHLC) for stock."""
        result: PreviousCloseAgg = self.client.get_previous_close_agg(ticker=ticker)
        if isinstance(result, HTTPResponse):
            raise PolygonAPIException(pformat(result))
        if isinstance(result, list):
            result = result[0]
        return {
            "ticker": result.ticker,
            "timestamp": date.fromtimestamp(result.timestamp / 1000).isoformat(),
            "open_price": result.open,
            "close_price": result.close,
            "highest_price": result.high,
            "lowest_price": result.low,
        }

    def _get_daily_bar(self, ticker: str, iso_date: str) -> dict:
        """Daily open, high, low, and close (OHLC) for stock."""
        result: DailyOpenCloseAgg = self.client.get_daily_open_close_agg(
            date=iso_date, ticker=ticker
        )
        if isinstance(result, HTTPResponse):
            raise PolygonAPIException(pformat(result))
        return {
            "ticker": result.symbol,
            "timestamp": date.fromisoformat(result.from_).isoformat(),
            "open_price": result.open,
            "close_price": result.close,
            "highest_price": result.high,
            "lowest_price": result.low,
        }

    def get_profit_range(self, ticker: str, iso_date: str) -> dict:
        prev = self._get_previous_close(ticker)
        bar = self._get_daily_bar(ticker, iso_date=iso_date)
        print(f"{bar}")
        print(f"{prev:}")
        return {
            "stock_bar": bar,
            "last_bar": prev,
            "ticker": ticker,
            "date": date.today().isoformat(),
            "min_change": f"{bar.get('highest_price') / prev.get('highest_price') * 100 - 100:.2f}",
            "max_change": f"{bar.get('lowest_price') / prev.get('highest_price') * 100 - 100:.2f}",
        }


if __name__ == "__main__":
    pass
