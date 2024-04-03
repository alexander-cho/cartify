
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
