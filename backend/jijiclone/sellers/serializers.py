from rest_framework import serializers
from sellers.models import Seller, Item, Buyer

# Seller serializer

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class SellerField(serializers.RelatedField):
    def to_representation(self, value):
        seller = {
            "name": value.first_name + ' ' + value.last_name,
            "location": value.state_of_residence,
            "email": value.email
        }
        return seller
class ItemSerializer(serializers.ModelSerializer):
    seller = SellerField(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'

    def create(self,validated_data):
        seller = Seller.objects.get(pk=self.context['pk'])
        validated_data['seller'] = seller
        return Item.objects.create(**validated_data)
    


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'