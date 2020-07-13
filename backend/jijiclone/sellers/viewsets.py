from .serializers import SellerSerializer, BuyerSerializer, ItemSerializer
from sellers.models import Seller, Buyer, Item
from rest_framework import viewsets, permissions

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ItemSerializer

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer