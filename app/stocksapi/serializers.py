"""Serializers module"""

from datetime import date

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from stocksapi.models import ProfitAndLoss, StockDailyBar
from stocksapi.polygon import ServiceLayer

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

    def create(self, validated_data: dict) -> ProfitAndLoss:
        """Override function."""
        profit_range = stock_service.get_profit_range(
            ticker=validated_data["ticker"],
            iso_date=validated_data["date"].isoformat(),
        )
        profit_range["stock_bar"] = StockDailyBar(**profit_range["stock_bar"])
        profit_range["last_bar"] = StockDailyBar(**profit_range["last_bar"])
        profit_range["stock_bar"].save()
        profit_range["last_bar"].save()
        pnl = ProfitAndLoss(**profit_range)
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
        if attrs.get("date") > date.today():
            raise ValidationError("Invalid `date`. It must be a past date.")
        return attrs
