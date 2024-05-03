from django.shortcuts import render

from store.models import Profile
from store.forms import UserInfoForm
from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingForm


# order checkout view
def checkout(request):
    order_items = OrderItem.objects.all()
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    return render(request, 'payment/checkout.html', {'order_items':order_items, 'shipping_form': shipping_form})


def payment_success(request):
    return render(request, 'payment/payment_success.html')
