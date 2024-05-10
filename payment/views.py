from django.shortcuts import render, redirect
from django.contrib import messages

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


def billing_info(request):
    # if user submitted form from previous page (shipping info)
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_contents = cart.get_cart()
        quantities = cart.get_quantities()  # dictionary- {product id: quantity}
        cart_total = cart.calculate_total()

        # check to see if user is logged in
        if request.user.is_authenticated:
            # shipping_info context is the previous post request that user submitted during checkout
            return render(request, 'payment/billing_info.html',{'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_info': request.POST})
        else:
            pass

        shipping_form = request.POST

        return render(request, 'payment/billing_info.html',{'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_form': shipping_form})
    else:
        messages.success(request, 'Access denied')
        return redirect('home')


def payment_success(request):
    return render(request, 'payment/payment_success.html')
