from rest_framework import serializers
from .models import Product, Cart

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class Cart(serializers.ModelSerializer):
    class Meta:
        model = Cart
        db_table = 'cart'
