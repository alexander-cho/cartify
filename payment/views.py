from django.shortcuts import render, redirect
from django.contrib import messages

from .models import ShippingAddress
from .forms import ShippingForm, PaymentForm

from cart.cart import Cart


# order checkout view
def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_contents = cart.get_cart_contents()
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
        cart_contents = cart.get_cart_contents()
        quantities = cart.get_quantities()  # dictionary- {product id: quantity}
        cart_total = cart.calculate_total()

        # create a session with shipping information
        my_shipping_info = request.POST
        request.session['my_shipping_info'] = my_shipping_info

        # check to see if user is logged in
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            # shipping_info context is the previous post request that user submitted during checkout
            return render(request, 'payment/billing_info.html',{'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',{'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_info': request.POST, 'billing_form': billing_form})
    else:
        messages.success(request, 'Access denied')
        return redirect('home')


def process_order(request):
    # make sure a post request was submitted from the billing info page
    if request.POST:
        # Get the cart total for order info
        cart = Cart(request)
        cart_contents = cart.get_cart_contents()
        quantities = cart.get_quantities()  # dictionary- {product id: quantity}
        cart_total = cart.calculate_total()

        # get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # get shipping info session data , it's been submitted in a previous form but not with the billing info
        my_shipping_info = request.session.get('my_shipping_info')
        print(my_shipping_info)

        # GATHER ORDER INFORMATION
        full_name = my_shipping_info['shipping_full_name']
        email = my_shipping_info['shipping_email']
        # using shipping info passed from request, create a single shipping address by concatenating session info
        shipping_address = f"{my_shipping_info['shipping_address1']}\n{my_shipping_info['shipping_address2']}\n{my_shipping_info['shipping_city']}\n{my_shipping_info['shipping_state']}\n{my_shipping_info['shipping_zipcode']}\n{my_shipping_info['shipping_country']}"
        amount_paid = cart_total

        if request.user.is_authenticated:
            # logged in
            user = request.user

        else:
            # not logged in
            pass

        messages.success(request, 'Order placed')
        return redirect('home')
    else:
        messages.success(request, 'Access denied')
        return redirect('home')

    # return render(request, 'payment/process_order.html')


def payment_success(request):
    return render(request, 'payment/payment_success.html')
