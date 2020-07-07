import json
import environ
from functools import reduce
from bill.models import Invoice
from checkout.models import Order
from bill.serializers import InvoiceSerializer
from bill.permissions import IsOwnerOrReadOnly
from datetime import datetime
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets

env = environ.Env(
    TAX_RATE=(int, 10),
    VAT_RATE=(int, 15),
)

# Create your views here.


class InvoiceList(APIView):
    """
    List all invoices, or create a new invoice.
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]

    def get(self, request, format=None):
        invoices = Invoice.objects.all().filter(deleted__isnull=True)
        serializer = InvoiceSerializer(
            invoices, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        request = load_invoice_parameters(request)
        serializer = InvoiceSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(order=request.order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetail(APIView):
    """
    Retrieve, update or delete a invoice instance.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Invoice.objects.filter(deleted__isnull=True).get(pk=pk)
        except Invoice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        invoice = self.get_object(pk)
        request = load_invoice_parameters(request)
        serializer = InvoiceSerializer(
            invoice, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        invoice = self.get_object(pk)
        invoice.deleted = datetime.now()
        invoice.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

def get_order(fk):
    try:
        return Order.objects.filter(deleted__isnull=True).get(pk=fk)
    except Order.DoesNotExist:
        raise Http404

def load_invoice_parameters(request):
    """
    This method creates an invoice object.
    """
    if isinstance(request.order, int):
        order = get_order(request.order)
    else:
        order = request.order
    products = json.loads(order.products)
    total = 0.0
    for product in products:
        total += product['cost'] * product['quantity']
    total = float("{:.2f}".format(total))
    sub_total = total
    taxes = float("{:.2f}".format(sub_total * float(env('TAX_RATE') / 100)))
    vat = float("{:.2f}".format(sub_total * float(env('VAT_RATE') / 100)))
    request.data['sub_total'] = sub_total
    request.data['taxes'] = taxes
    request.data['vat'] = vat
    request.data['total'] = total + taxes + vat
    return request