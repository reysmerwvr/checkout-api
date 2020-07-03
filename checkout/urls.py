from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from checkout import views

urlpatterns = [
    path('orders', views.order_list),
    path('orders/<int:pk>', views.order_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)