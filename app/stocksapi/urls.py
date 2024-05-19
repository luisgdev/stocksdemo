"""URLs module"""

from django.urls import path

from stocksapi import views

urlpatterns = [
    path("pnl/", views.PNLListCreateView.as_view()),
    path("pnl/<str:id>/", views.PNLReadDeleteView.as_view()),
    path("stock/", views.StockListView.as_view()),
    path("stock/<str:id>/", views.StockReadDeleteView.as_view()),
]
