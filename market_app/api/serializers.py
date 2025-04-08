from rest_framework import serializers
from market_app.models import Market, Seller, Product
import re

def validate_text_field(value):
    if any(char.isdigit() for char in value):
        raise serializers.ValidationError("Dieses Feld darf keine Zahlen enthalten.")
    if not re.match(r'^[a-zA-ZäöüÄÖÜß\s-]+$', value):
        raise serializers.ValidationError("Only letters, spaces and hyphens allowed.")
    return value


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length=255, required=False, validators = [validate_text_field])
    location = serializers.CharField(max_length=255, required=False, validators = [validate_text_field])
    description = serializers.CharField(required=False, validators = [validate_text_field])
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2, required=False)


    def create(self, validated_data):
        return Market.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance
    
class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(many=True, read_only=True)
    markets = serializers.StringRelatedField(many = True)


class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if markets.count() != len(value):
            raise serializers.ValidationError("One or more Market IDs not found")
        return value

    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets)
        return seller

 
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.IntegerField()
    seller = serializers.IntegerField()

    def validate_market(self, value):
        if not Market.objects.filter(id=value).exists():
            raise serializers.ValidationError("Market ID not found")
        return value

    def validate_seller(self, value):
        if not Seller.objects.filter(id=value).exists():
            raise serializers.ValidationError("Seller ID not found")
        return value

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.market_id = validated_data.get('market', instance.market_id)
        instance.seller_id = validated_data.get('seller', instance.seller_id)
        instance.save()
        return instance



    
