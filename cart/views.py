from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product

# Create your views here.

def cart_overview(request):
    cart = Cart(request)
    cart_contents = cart.get_cart()
    quantities = cart.get_quantities() # dictionary- {product id: quantity}
    cart_total = cart.calculate_total()
    return render(request, 'cart/overview.html', {'cart_contents': cart_contents, 'quantities': quantities, 'cart_total': cart_total})


def add_to_cart(request):
    # retrieve the cart instance
    cart = Cart(request)

    # test for a POST request
    if request.POST.get('action') == 'post': # action from product page jquery script
        # get the item
        product_id = int(request.POST.get('product_id'))

        # get the quantity
        product_quantity = int(request.POST.get('product_quantity'))

        # look up product in DB
        product = get_object_or_404(Product, id=product_id)

        # save to session
        cart.add(product=product, quantity=product_quantity)

        # get cart quantity
        cart_quantity = cart.__len__()

        # return response
        # response = JsonResponse({'Product name: ': product.name})
        response = JsonResponse({'quantity': cart_quantity}) # passed into jquery success function store/product.html

        return response


def update_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product=product_id, quantity=product_quantity)

        response = JsonResponse({'newquantity': product_quantity})
        return response
    
        

def delete_from_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)
        
        response = JsonResponse({'you have removed': product_id})
        return response
    


