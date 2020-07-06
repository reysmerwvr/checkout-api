from bill.models import Invoice
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

# Create your views here.


class InvoiceList(APIView):
    """
    List all invoices, or create a new order.
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
        serializer = InvoiceSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(order=request.order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetail(APIView):
    """
    Retrieve, update or delete a order instance.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = InvoiceSerializer(order, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = InvoiceSerializer(
            order, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.deleted = datetime.now()
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)