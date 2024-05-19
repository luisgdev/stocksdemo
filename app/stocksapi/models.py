"""Models module"""

from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    Model,
)


class StockDailyBar(Model):
    """Daily open, high, low, and close (OHLC) bar for stock."""

    ticker = CharField(max_length=12, blank=False, null=False)
    timestamp = DateField(null=True, blank=True)
    open_price = FloatField(blank=False, null=False)
    close_price = FloatField(blank=False, null=False)
    highest_price = FloatField(blank=False, null=False)
    lowest_price = FloatField(blank=False, null=False)


class ProfitAndLoss(Model):
    """Profit and Loss Indicator"""

    date = DateField(null=True, blank=True)
    ticker = CharField(max_length=12, blank=False, null=False, default="")
    min_change = FloatField(blank=False, null=False)
    max_change = FloatField(blank=False, null=False)
    stock_bar = ForeignKey(StockDailyBar, related_name="stock_bar", on_delete=CASCADE)
    last_bar = ForeignKey(StockDailyBar, related_name="last_bar", on_delete=CASCADE)
