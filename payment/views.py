from django.shortcuts import render, redirect
from django.contrib import messages

from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingForm, PaymentForm

from cart.cart import Cart


# order checkout view
def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_contents = cart.get_cart_contents()
    # item quantities is a dictionary of {product id: quantity}
    quantities = cart.get_quantities()
    cart_total = cart.calculate_total()

    if request.user.is_authenticated:
        # checkout as member
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_form': shipping_form})
    else:
        # checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_form': shipping_form})


def billing_info(request):
    # if user submitted form from previous page (shipping info)
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_contents = cart.get_cart_contents()
        # item quantities is a dictionary of {product id: quantity}
        quantities = cart.get_quantities()
        cart_total = cart.calculate_total()

        # create a session with shipping information
        my_shipping_info = request.POST
        request.session['my_shipping_info'] = my_shipping_info

        # check to see if user is logged in
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            # shipping_info context is the previous post request that user submitted during checkout
            return render(request, 'payment/billing_info.html', {'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total, 'shipping_info': request.POST, 'billing_form': billing_form})
    else:
        messages.success(request, "Access denied")
        return redirect('home')


def process_order(request):
    # make sure a post request was submitted from the billing info page
    if request.POST:
        # Get the cart total for order info
        cart = Cart(request)
        cart_contents = cart.get_cart_contents()
        quantities = cart.get_quantities()
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

        # CREATE AN ORDER
        if request.user.is_authenticated:
            # if logged in
            user = request.user
            # create order using attributes defined above
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # CREATE ORDER ITEMS (assign model foreign keys)
            # get the id of the order
            order_id = create_order.id
            # get product info
            for item in cart_contents:
                # get product id
                product_id = item.id
                # get product price
                if item.is_on_sale:
                    price = item.sale_price
                else:
                    price = item.price

                # get quantities
                for k, v in quantities.items():
                    # change k, the key in the cart "dictionary" to an int since it's originally a string
                    if int(k) == product_id:
                        # create an order item
                        create_order_item = OrderItem(order_id=order_id, products_id=product_id, user=user, quantity=v, price=price)
                        create_order_item.save()

            messages.success(request, "Order placed")
            return redirect('home')
        else:
            # not logged in, create order without user definition
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # CREATE ORDER ITEMS (assign model foreign keys)
            # get the id of the order
            order_id = create_order.id
            # get product info
            for item in cart_contents:
                # get product id
                product_id = item.id
                # get product price
                if item.is_on_sale:
                    price = item.sale_price
                else:
                    price = item.price

                # get quantities
                for k, v in quantities.items():
                    # change k, the key in the cart "dictionary" to an int since it's originally a string
                    if int(k) == product_id:
                        # create an order item
                        create_order_item = OrderItem(order_id=order_id, products_id=product_id, quantity=v, price=price)
                        create_order_item.save()

            messages.success(request, "Order placed")
            return redirect('home')
    else:
        messages.success(request, "Access denied")
        return redirect('home')

    # return render(request, 'payment/process_order.html')


def payment_success(request):
    return render(request, 'payment/payment_success.html')
