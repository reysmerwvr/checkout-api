from django.urls import path
from checkout import views

urlpatterns = [
    path('orders/', views.order_list),
    path('orders/<int:pk>/', views.order_detail),
]