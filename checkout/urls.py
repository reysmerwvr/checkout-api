from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from checkout import views

urlpatterns = [
    path('', views.checkout_api),
    path('orders', views.OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),
    path('users', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
