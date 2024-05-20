"""Serializers module"""

import logging
from datetime import date

from django.db.models import ObjectDoesNotExist
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.serializers import ModelSerializer

from stocksapi.models import ProfitAndLoss, StockDailyBar
from stocksapi.polygon import ServiceLayer
from stocksapi.utils import get_last_business_day

stock_service = ServiceLayer()


class PNLSerializer(ModelSerializer):
    """Stock Day Serializer"""

    class Meta:
        model = ProfitAndLoss
        fields = "__all__"


class StockSerializer(ModelSerializer):
    """Stock Day Serializer"""

    class Meta:
        model = StockDailyBar
        fields = "__all__"


class PNLDetailSerializer(ModelSerializer):
    """Stock Day Serializer"""

    class Meta:
        model = ProfitAndLoss
        fields = "__all__"
        read_only_fields = ("stock_bar", "last_bar", "min_change", "max_change")

    def to_representation(self, instance) -> dict:
        """Override function."""
        data: dict = super().to_representation(instance)
        data["stock_bar"] = StockDailyBar.objects.filter(id=instance.stock_bar.id).values()
        data["last_bar"] = StockDailyBar.objects.filter(id=instance.last_bar.id).values()
        return data

    def create(self, validated_data: dict) -> ProfitAndLoss:
        """Override function."""
        if _check_pnl_existence(
            ticker=validated_data["ticker"],
            date_=validated_data["date"],
        ):
            raise APIException("PNL object already exists.")

        result = {"ticker": validated_data["ticker"]}
        stock_bar = _get_stock_bar(
            ticker=validated_data["ticker"], iso_date=validated_data["date"].isoformat()
        )
        if not stock_bar:
            raise APIException("Data not found for given date.")

        last_bar = _get_last_bar(ticker=validated_data["ticker"])
        result["stock_bar"] = stock_bar
        result["last_bar"] = last_bar
        result["date"] = last_bar.timestamp
        profit_range = _calculate_profit_range(stock_bar=stock_bar, last_bar=last_bar)
        result.update(profit_range)
        pnl = ProfitAndLoss(**result)
        pnl.save()
        return pnl

    def validate(self, attrs: dict) -> dict:
        """Validate ProfitAndLoss attributes"""
        if not attrs.get("date"):
            raise ValidationError("Error: `date` parameter is missing")
        if not attrs.get("ticker"):
            raise ValidationError("Error: `ticker` parameter is missing")
        if not attrs.get("ticker").isalpha():
            raise ValidationError("Invalid `ticker`. It must contain letters only.")
        if attrs.get("date") >= date.today():
            raise ValidationError("Invalid `date`. It must be a past date.")
        return attrs


def _calculate_profit_range(stock_bar: StockDailyBar, last_bar: StockDailyBar) -> dict:
    """Calculate Profit Range"""
    return {
        "min_change": f"{stock_bar.lowest_price / last_bar.highest_price * 100 - 100:.2f}",
        "max_change": f"{stock_bar.highest_price / last_bar.highest_price * 100 - 100:.2f}",
    }


def _get_stock_bar(ticker: str, iso_date: str) -> StockDailyBar | None:
    """Retrieve Stock bar for a given date and ticker"""
    try:
        stock_bar = StockDailyBar.objects.get(
            ticker=ticker,
            timestamp=get_last_business_day(day=iso_date),
        )
        return stock_bar
    except ObjectDoesNotExist as ex:
        logging.error(ex, iso_date)
    try:
        stock_bar = StockDailyBar(
            **stock_service.get_daily_bar(
                ticker=ticker,
                iso_date=get_last_business_day(day=iso_date),
            )
        )
        stock_bar.save()
        return stock_bar
    except Exception as ex:
        logging.error(ex, iso_date)
    return None


def _get_last_bar(ticker: str) -> StockDailyBar:
    """Retrieve Last bar for a given ticker"""
    try:
        prev_bar = StockDailyBar.objects.get(
            ticker=ticker,
            timestamp=get_last_business_day(day=date.today()).isoformat(),
        )
    except ObjectDoesNotExist as _:
        prev_bar = StockDailyBar(
            **stock_service.get_previous_close(
                ticker=ticker,
            )
        )
        prev_bar.save()
    return prev_bar


def _check_pnl_existence(ticker, date_) -> bool:
    """Check if PNL already exists"""
    if not _check_stock_bar_existence(ticker=ticker, date_=get_last_business_day(day=date_)):
        return False
    if not _check_stock_bar_existence(
        ticker=ticker, date_=get_last_business_day(day=date.today())
    ):
        return False
    return True


def _check_stock_bar_existence(ticker, date_) -> bool:
    """Check if a stock bar exists"""
    try:
        StockDailyBar.objects.get(ticker=ticker, timestamp=get_last_business_day(day=date_))
    except ObjectDoesNotExist as _:
        return False
    return True
