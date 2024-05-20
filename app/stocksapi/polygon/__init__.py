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

    def get_previous_close(self, ticker: str) -> dict:
        """Get the previous day's open, high, low, and close (OHLC) for stock."""
        result: PreviousCloseAgg = self.client.get_previous_close_agg(ticker=ticker)
        print(result)
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

    def get_daily_bar(self, ticker: str, iso_date: str) -> dict:
        """Daily open, high, low, and close (OHLC) for stock."""
        result: DailyOpenCloseAgg = self.client.get_daily_open_close_agg(
            date=iso_date, ticker=ticker
        )
        print(result)
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


if __name__ == "__main__":
    pass
