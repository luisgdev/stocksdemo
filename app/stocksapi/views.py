"""Views module"""

from rest_framework import generics, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from stocksapi.models import ProfitAndLoss, StockDailyBar
from stocksapi.serializers import PNLSerializer, PNLDetailSerializer, StockSerializer

AUTH_CLASSES = (
    BasicAuthentication,
    SessionAuthentication,
)


class PNLListCreateView(generics.ListCreateAPIView):
    """List and Create PNL objects."""

    queryset = ProfitAndLoss.objects.all()
    authentication_classes = AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PNLDetailSerializer


class PNLReadDeleteView(generics.RetrieveDestroyAPIView):
    """Retrieve and Destroy PNL objects"""

    lookup_field = "id"
    queryset = ProfitAndLoss.objects.all()
    authentication_classes = AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PNLSerializer


class StockListView(generics.ListAPIView):
    """List Stock objects."""

    queryset = StockDailyBar.objects.all()
    authentication_classes = AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StockSerializer


class StockReadDeleteView(generics.RetrieveDestroyAPIView):
    """Retrieve and Destroy Stock objects"""

    lookup_field = "id"
    queryset = StockDailyBar.objects.all()
    authentication_classes = AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StockSerializer
