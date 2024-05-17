"""Serializers module"""

from django.db.models.query import QuerySet
from rest_framework.serializers import ModelSerializer, ValidationError

from stocksapi.models import StockDayBar
from stocksapi.polygon import ServiceLayer

stock_service = ServiceLayer()


class StockDayBarSerializer(ModelSerializer):
    """Stock Day Bar serializer"""

    class Meta:
        model = StockDayBar
        fields = "ticker"

    def create(self, validated_data: dict) -> StockDayBar:
        """Override function. To add `final_price`."""
        prev_close = stock_service.get_previous_close(validated_data["ticker"]).__dict__
        stock_day_bar = StockDayBar(**prev_close)
        # stock_day_bar.save()
        return stock_day_bar
