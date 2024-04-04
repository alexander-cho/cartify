from store.models import Product


class Cart():
    def __init__(self, request) -> None:
        # session object associated with current request
        self.session = request.session

        # get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, create a session key since it doesn't exist yet
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available accross entire application - (apps/pages)
        self.cart = cart


    def get_cart(self):
        # get ids from cart
        product_ids = self.cart.keys() # set up as dictionary as defined in product template jquery and add view {product_id: price}
        # use ids to look up products in DB model
        products = Product.objects.filter(id__in=product_ids)
        return products


    def add(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'Price:': str(product.price)}
        
        self.session.modified = True



    '''
    return the length of the cart
    '''
    def __len__(self):
        return len(self.cart)
