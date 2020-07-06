from django.db import models
from checkout.models import Order

# Create your models here.


class Invoice(models.Model):
    """Invoice Data model
        """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=255, null=True)
    sub_total = models.DecimalField(max_digits=7, decimal_places=2, null=False)
    taxes = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    vat = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, null=True)
    deleted = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.id
