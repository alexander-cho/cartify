from .cart import Cart


# create context processor so cart works on all pages
def cart(request):
    """
    Here, we initialize the Cart object with the request and return it in a dictionary
    This ensures that the cart object is available in the context of all templates
    """
    return {'cart': Cart(request)}
