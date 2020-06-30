import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Order(models.Model):
	"""Data model of an Order
	"""
	clientId = models.ForeignKey(
		'User',
		on_delete=models.CASCADE
	)
	date = models.DateTimeField(auto_now=True)
	direction = models.TextField()
	products = models.TextField()

	def __str__(self):
		return self.direction

	def was_ordered_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.date <= now

	was_ordered_recently.admin_order_field = 'date'
	was_ordered_recently.boolean = True
	was_ordered_recently.short_description = 'ordered recently?'



class User(AbstractUser):
	"""Data model of an User
	"""
	orders = models.ManyToManyField(Order)

	def __str__(self):
		return self.user

	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def create_auth_token(self, sender, instance=None, created=False, **kwargs):
		if created:
			Token.objects.create(user=instance)
