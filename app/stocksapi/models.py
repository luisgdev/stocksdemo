"""Models module"""

from django.db.models import Model, CharField, FloatField, DateField


class StockDayBar(Model):
    """Daily open, high, low, and close (OHLC) for stock."""
    ticker = CharField(max_length=12, blank=False, null=False)
    timestamp = DateField(null=True, blank=True)
    open_price = FloatField(blank=False, null=False)
    close_price = FloatField(blank=False, null=False)
    highest_price = FloatField(blank=False, null=False)
    lowest_price = FloatField(blank=False, null=False)
    tx_quantity = FloatField(blank=False, null=False)


class StockTrade(Model):
    """Investment performance for a stock."""
    stock_before = StockDayBar
    stock_after = StockDayBar
    min_profit = FloatField(blank=False, null=False)
    max_profit = FloatField(blank=False, null=False)
