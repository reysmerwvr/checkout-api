from checkout.views import UserViewSet, OrderList, OrderDetail, checkout_api
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path


user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('', checkout_api),
    path('orders', OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>', OrderDetail.as_view(), name='order-detail'),
    path('users', user_list, name='user-list'),
    path('users/<int:pk>', user_detail, name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
