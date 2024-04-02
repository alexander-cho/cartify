
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