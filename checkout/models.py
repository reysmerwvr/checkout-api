import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Order(models.Model):
	"""Data model of an Order
	"""
	client = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)
	direction = models.TextField()
	products = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	deleted = models.DateTimeField(auto_now_add=False, null=True)

	def __str__(self):
		return self.direction

	def was_ordered_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.date <= now

	was_ordered_recently.admin_order_field = 'date'
	was_ordered_recently.boolean = True
	was_ordered_recently.short_description = 'ordered recently?'

	class Meta:
		ordering = ['created']

