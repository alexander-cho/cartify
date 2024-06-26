import datetime

from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class ShippingAddress(models.Model):
    """
    Shipping address associated with each user. User ability to update via form
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


def create_shipping_address(sender: any, instance: User, created: bool, **kwargs: any) -> None:
    """
    Create an empty shipping address associated with a user upon registration.

    Parameters:
    sender: The User class sends the signal
    instance: refers to the instance created of the data when register form is submitted
    created: indicates if a new instance of the sender class (User) was created

    Returns:
    None
    """
    if created:  # if a user has been created
        user_shipping_address = ShippingAddress(user=instance)
        user_shipping_address.save()


# automate signal
post_save.connect(create_shipping_address, sender=User)


# overall order
class Order(models.Model):
    """
    Order model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # blank if checking out as guest
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    shipping_address = models.TextField(max_length=1000)  # shipping label combine address related fields in shipping address model
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order of: {str(self.id)}-{self.full_name}'


# Automatically add shipping date when is_shipped becomes True
@receiver(pre_save, sender=Order)
def save_shipped_date(sender, instance, **kwargs):
    # verify that the Order instance exists by looking for its primary key,
    # ensuring signal only processes updates to existing orders, not new orders.
    if instance.pk:
        current_time = datetime.datetime.now()
        # retrieve current state of the order
        obj = sender._default_manager.get(pk=instance.pk)
        # set to True
        if instance.is_shipped and not obj.is_shipped:
            instance.date_shipped = current_time


class OrderItem(models.Model):
    """
    Represents a single item in the order. When the customer checks out, an Order is generated, and everything they
    purchase becomes an OrderItem, as defined below.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)  # which order does it belong to
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)  # what products are being purchased in this order
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)  # there has to be one thing at least in an order
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'Order item: {str(self.id)}'
