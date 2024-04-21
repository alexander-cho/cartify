from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # associate User
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100, null=True, blank=True)

    # don't pluralize address
    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping Address: {str(self.id)}'
