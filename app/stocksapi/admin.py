"""Admin module"""

from django.contrib import admin

from stocksapi.models import ProfitAndLoss, StockDailyBar

# Register your models here.
admin.site.register(StockDailyBar)
admin.site.register(ProfitAndLoss)
