from django.contrib import admin
from django.contrib.auth.models import User

from .models import ShippingAddress, Order, OrderItem


admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# create an order item inline
class OrderItemInline(admin.StackedInline):
    """
    We create an inline for the OrderItem model so that we can display order items and its attributes within the Order,
    which is a different model, and to be able to edit each OrderItem in that Order (parent model)
    """
    model = OrderItem
    # no extra fields, meaning items that have not been ordered showing up
    extra = 0


# extend Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]


# unregister old Order model
admin.site.unregister(Order)


# re-register Order and OrderItem to account for inline changes
admin.site.register(Order, OrderAdmin)
