"""Polygon API Module"""

import os
from pprint import pformat
from urllib3.response import HTTPResponse
from polygon import RESTClient
from polygon.rest.models.aggs import GroupedDailyAgg, PreviousCloseAgg
from dotenv import load_dotenv

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

    def get_previous_close(self, ticker: str) -> PreviousCloseAgg:
        """Get the previous day's open, high, low, and close (OHLC) for stock."""
        result: PreviousCloseAgg = self.client.get_previous_close_agg(ticker=ticker)
        if isinstance(result, HTTPResponse):
            raise PolygonAPIException(pformat(result))
        if isinstance(result, list):
            return result[0]
        return result

    def get_daily_bar(self, ticker: str, iso_date: str) -> GroupedDailyAgg:
        """Daily open, high, low, and close (OHLC) for stock."""
        result: list[GroupedDailyAgg] = self.client.get_grouped_daily_aggs(date=iso_date)
        if isinstance(result, HTTPResponse):
            raise PolygonAPIException(pformat(result))
        for item in result:
            if item.ticker == ticker:
                return item
        raise PolygonAPIException(f"Stock ticker '{ticker}' was not found.")

    def get_profit_range(self, ticker: str, iso_date: str) -> dict:
        prev = self.get_previous_close(ticker)
        bar = self.get_daily_bar(ticker, iso_date=iso_date)
        return {
            "min": f"{bar.high / prev.high * 100 - 100:.2f}",
            "max": f"{bar.low / prev.low * 100 - 100:.2f}",
        }


if __name__ == "__main__":
    pass
