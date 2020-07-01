from rest_framework import serializers
from django.conf import settings
from checkout.models import Order
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    direction = serializers.CharField()
    products = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    deleted_at = serializers.DateTimeField()


    def create(self, validated_data):
        """
        Create and return a new `Order` instance, given the validated data.
        """
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Order` instance, given the validated data.
        """
        instance.direction = validated_data.get('direction', instance.direction)
        instance.products = validated_data.get('products', instance.products)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.save()
        return instance

    class Meta:
        model = Order
        fields = ['id', 'direction', 'products', 'created_at']


class UserSerializer(serializers.Serializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'username', 'email', 'groups']