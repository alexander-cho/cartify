from .cart import Cart


# create context processor so cart works on all pages
def cart(request):
    # return default data from cart
    return {'cart': Cart(request)}
