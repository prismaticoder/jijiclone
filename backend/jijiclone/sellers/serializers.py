from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from sellers.models import Seller, Item, Buyer


# Seller serializer

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Seller.objects.create(**validated_data)

class SellerField(serializers.RelatedField):
    def to_representation(self, value):
        seller = {
            "name": value.first_name + ' ' + value.last_name,
            "location": value.state_of_residence,
            "email": value.email
        }
        return seller

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

    def create(self, validated_data):
        item = Item.objects.get(slug=self.context['slug'])
        buyer = Buyer.objects.create(**validated_data)
        
        item.interested_buyers.add(buyer)
        return buyer

class ItemSerializer(serializers.ModelSerializer):
    seller = SellerField(read_only=True)
    interested_buyers = BuyerSerializer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = '__all__'

    def create(self,validated_data):
        seller = Seller.objects.get(pk=self.context['pk'])
        validated_data['seller'] = seller
        return Item.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.is_sold = validated_data.get('is_sold', instance.is_sold)
        instance.imageUrl = validated_data.get('imageUrl', instance.imageUrl)
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            checkuser = Seller.objects.get(email=data['email'])

            if check_password(data['password'], checkuser.password):
                return SellerSerializer(checkuser).data
            raise serializers.ValidationError(detail={"error": "Incorrect username or password"})

        except Seller.DoesNotExist:
            raise serializers.ValidationError(detail={"error": "Incorrect username or password"})