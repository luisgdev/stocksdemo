"""Admin module"""

from django.contrib import admin
from stocksapi.models import StockDayBar, StockTrade

# Register your models here.
admin.site.register(StockDayBar)
admin.site.register(StockTrade)
