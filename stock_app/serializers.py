from rest_framework import serializers
from .models import Stock, UserStock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'symbol', 'company_name']

    id = serializers.IntegerField(read_only=True, help_text="The unique identifier for a stock")
    symbol = serializers.CharField(help_text="The stock symbol")
    company_name = serializers.CharField(help_text="The name of the company")

class UserStockSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True, help_text="The username of the stock owner")
    symbol = serializers.CharField(source='stock.symbol', read_only=True, help_text="The stock symbol")

    class Meta:
        model = UserStock
        fields = ['id', 'user_name', 'symbol']

    id = serializers.IntegerField(read_only=True, help_text="The unique identifier for a user's stock")