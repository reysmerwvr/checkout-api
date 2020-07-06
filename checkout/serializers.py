import json
from datetime import datetime
from rest_framework import serializers
from django.conf import settings
from checkout.models import Order
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    direction = serializers.CharField()
    products = serializers.JSONField()
    created = serializers.DateTimeField(required=False, initial=datetime.now())
    updated = serializers.DateTimeField(required=False, allow_null=True)
    deleted = serializers.DateTimeField(required=False, allow_null=True)
    client = serializers.HyperlinkedRelatedField(
        many=False,
        allow_null=False,
        read_only=True,
        view_name='user-detail'
    )

    def to_representation(self, value):
        """Convert `products` to json."""
        ret = super().to_representation(value)
        ret['products'] = json.loads(ret['products'])
        return ret

    def to_internal_value(self, data):
        """Convert `products` to string."""
        if 'products' in data:
            data['products'] = json.dumps(data['products'])
        return super().to_internal_value(data)

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
        instance.updated = validated_data.get(
            'updated', datetime.now())
        instance.save()
        return instance

    class Meta:
        model = Order
        fields = ['id', 'direction', 'products',
                'created', 'updated', 'deleted', 'client']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    orders = serializers.HyperlinkedRelatedField(
        many=True, view_name='order-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'orders']
