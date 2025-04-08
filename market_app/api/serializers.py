from rest_framework import serializers
from market_app.models import Market, Seller, Product
import re


class MarketSerializer(serializers.ModelSerializer):
    
    sellers = serializers.HyperlinkedRelatedField(
    many=True,
    read_only=True,
    view_name = "seller_single"
)

    
    
    class Meta:
        model = Market
        exclude = []

    def validate_name(self, value):
        if not re.match(r'^[a-zA-ZäöüÄÖÜß\s-]+$', value):
            raise serializers.ValidationError("Name may only contain letters, spaces, and hyphens.")
        return value

    def validate_description(self, value):
        if not re.match(r'^[a-zA-ZäöüÄÖÜß\s-]+$', value):
            raise serializers.ValidationError("Description may only contain letters, spaces, and hyphens.")
        return value

    def validate_location(self, value):
        if not re.match(r'^[a-zA-ZäöüÄÖÜß\s-]+$', value):
            raise serializers.ValidationError("Location may only contain letters, spaces, and hyphens.")
        return value


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)

    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(),
        many=True,
        write_only=True,
        source='markets'
    )

    market_count = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'contact_info', 'markets', 'market_ids', 'market_count']

    def get_market_count(self, obj):
        return obj.markets.count()

    def validate_markets(self, value):
        if len(value) != Market.objects.filter(id__in=[m.id for m in value]).count():
            raise serializers.ValidationError("One or more Market IDs not found")
        return value

    def create(self, validated_data):
        seller = Seller.objects.create(**validated_data)
        markets = validated_data.get('markets', [])
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
