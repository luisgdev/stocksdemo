"""Views module"""

from rest_framework import generics, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from stocksapi.models import StockDayBar
from stocksapi.serializers import StockDayBarSerializer

AUTH_CLASSES = (
    BasicAuthentication,
    SessionAuthentication,
)


class StockBarView(generics.ListAPIView):
    """List Stock objects."""

    queryset = StockDayBar.objects.all()
    authentication_classes = AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StockDayBarSerializer
