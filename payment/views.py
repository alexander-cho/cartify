from django.shortcuts import render

from .models import ShippingAddress
from .forms import ShippingForm

from cart.cart import Cart


# order checkout view
def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_contents = cart.get_cart()
    quantities = cart.get_quantities()  # dictionary- {product id: quantity}
    cart_total = cart.calculate_total()

    if request.user.is_authenticated:
        # checkout as member
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',{'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_form': shipping_form})
    else:
        # checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',{'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_form': shipping_form})


def payment_success(request):
    return render(request, 'payment/payment_success.html')
