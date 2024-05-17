"""URLs module"""

from django.urls import path
from stocksapi import views

urlpatterns = [
    # Property
    path("stocks/", views.StockBarView.as_view()),
]
