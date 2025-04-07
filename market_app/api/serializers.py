from rest_framework import serializers
from market_app.models import Market

class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 255)
    location = serializers.CharField(max_length = 255)
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits = 100, decimal_places = 2)


    def create(self, validated_data):
        return Market.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance
    
