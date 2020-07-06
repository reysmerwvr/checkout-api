from bill.views import InvoiceList, InvoiceDetail
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path


urlpatterns = [
    path('invoices', InvoiceList.as_view(), name='invoice-list'),
    path('invoices/<int:pk>', InvoiceDetail.as_view(), name='invoice-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)