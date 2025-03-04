from django.db import models
from django.contrib.auth.models import User
from HOME.models import Products
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import localtime, now


class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	shipping_full_name = models.CharField(max_length=255)
	shipping_email = models.CharField(max_length=255)
	shipping_address1 = models.CharField(max_length=255)
	shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
	shipping_city = models.CharField(max_length=255)
	shipping_state = models.CharField(max_length=255, null=True, blank=True)
	shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
	shipping_country = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "Shipping Address"

	def __str__(self):
		return f"Shipping Address- {str(self.id)}"


# Create your models here.
class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	shipping_address = models.TextField(max_length=15000)
	amount_paid = models.DecimalField(max_digits=100, decimal_places=2)
	order_date = models.DateTimeField(auto_now_add=True)
	shipped = models.BooleanField(default=False)
	date_shipped = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return f"Order- {str(self.id)}"


# Create Order Item Model
class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"Order Item- {str(self.id)}"


@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
	if instance.pk:
		previous_order = Order.objects.filter(pk=instance.pk).first()
		if previous_order and not previous_order.shipped and instance.shipped:
			instance.date_shipped = localtime(now())
