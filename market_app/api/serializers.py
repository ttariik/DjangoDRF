from rest_framework import serializers
from market_app.models import Market
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
    





    
