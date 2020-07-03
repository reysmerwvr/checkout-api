from datetime import datetime

from rest_framework import serializers
from django.conf import settings
from checkout.models import Order
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    direction = serializers.CharField()
    products = serializers.JSONField()
    created = serializers.DateTimeField(required=False, initial=datetime.now())
    updated = serializers.DateTimeField(required=False, allow_null=True)
    deleted = serializers.DateTimeField(required=False, allow_null=True)
    client = serializers.PrimaryKeyRelatedField(
        many=False, allow_null=False, queryset=User.objects.all())

    def create(self, validated_data):
        """
        Create and return a new `Order` instance, given the validated data.
        """
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Order` instance, given the validated data.
        """
        instance.direction = validated_data.get(
            'direction', instance.direction)
        instance.products = validated_data.get('products', instance.products)
        instance.updated_at = validated_data.get(
            'updated_at', instance.updated_at)
        instance.save()
        return instance

    class Meta:
        model = Order
        fields = ['id', 'direction', 'products',
                'created', 'updated', 'deleted', 'client']


class UserSerializer(serializers.Serializer):
    orders = serializers.HyperlinkedRelatedField(
        many=True, view_name='order-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'orders']
