from rest_framework import serializers
from datetime import datetime, date
from bill.models import Invoice


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField(required=False, initial=date.today())
    description = serializers.CharField(
        max_length=255, required=False, allow_null=True)
    sub_total = serializers.DecimalField(
        max_digits=7, decimal_places=2, allow_null=False)
    taxes = serializers.DecimalField(
        max_digits=7, decimal_places=2, allow_null=True)
    vat = serializers.DecimalField(
        max_digits=7, decimal_places=2, allow_null=True)
    total = serializers.DecimalField(
        max_digits=7, decimal_places=2, allow_null=False)
    created = serializers.DateTimeField(required=False, initial=datetime.now())
    updated = serializers.DateTimeField(required=False, allow_null=True)
    deleted = serializers.DateTimeField(required=False, allow_null=True)
    order = serializers.HyperlinkedRelatedField(
        many=False,
        allow_null=False,
        read_only=True,
        view_name='order-detail'
    )

    def create(self, validated_data):
        """
        Create and return a new `Invoice` instance, given the validated data.
        """
        return Invoice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Invoice` instance, given the validated data.
        """
        instance.description = validated_data.get(
            'description', instance.description)
        instance.sub_total = validated_data.get(
            'sub_total', instance.sub_total)
        instance.taxes = validated_data.get(
            'taxes', instance.taxes)
        instance.vat = validated_data.get(
            'vat', instance.vat)
        instance.total = validated_data.get(
            'total', instance.total)
        instance.updated = validated_data.get(
            'updated', datetime.now())
        instance.save()
        return instance

    class Meta:
        model = Invoice
        fields = ['id', 'date', 'description', 'sub_total',
                'taxes', 'vat', 'total', 'created', 'updated',
                'deleted', 'order']
