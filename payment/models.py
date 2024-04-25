from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.


class ShippingAddress(models.Model):
    """
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # associate User
    shipping_full_name = models.CharField(max_length=100)
    shipping_email = models.EmailField(max_length=100)
    shipping_address1 = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100, null=True, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_country = models.CharField(max_length=100)
    shipping_zipcode = models.CharField(max_length=100, null=True, blank=True)

    # don't pluralize address
    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping Address: {str(self.id)}'


# overall order
class Order(models.Model):
    """
    Order model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    shipping_address = models.TextField(max_length=1000)  # shipping label combine address related fields in shipping address model
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order of: {str(self.id)}-{self.full_name}'


class OrderItem(models.Model):
    """
    Represents a single item in the order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)  # what products are being purchased in this order
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)  # there has to be one thing at least in an order
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'Order item: {str(self.id)}'
