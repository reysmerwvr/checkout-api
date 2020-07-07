from checkout.models import Order
from bill.models import Invoice
from checkout.serializers import OrderSerializer
from checkout.serializers import UserSerializer
from checkout.permissions import IsOwnerOrReadOnly
from functools import reduce
from bill.views import InvoiceList, InvoiceDetail
from django.contrib.auth.models import User
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


class OrderList(APIView):
    """
    List all orders, or create a new order.
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]

    def get(self, request, format=None):
        orders = Order.objects.all().filter(deleted__isnull=True)
        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save(client=request.user)
            request.order = order
            invoice_list = InvoiceList()
            invoice_list.post(request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    """
    Retrieve, update or delete a order instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Order.objects.filter(deleted__isnull=True).get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get_invoice(self, order):
        try:
            return Invoice.objects.filter(deleted__isnull=True).get(order=order)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(
            order, data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save(client=request.user)
            request.order = order
            invoice = self.get_invoice(order)
            invoice_detail = InvoiceDetail()
            invoice_detail.patch(request, pk=invoice.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.deleted = datetime.now()
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super(UserViewSet, self).get_serializer_context()
        context.update({'request': self.request})
        return context


@api_view(['GET'])
def checkout_api(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'invoices': reverse('invoice-list', request=request, format=format)
    })


