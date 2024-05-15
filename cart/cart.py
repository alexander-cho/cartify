from store.models import Product, Profile


class Cart:
    """
    Cart class, to be accessed throughout the application using user sessions.
    """
    def __init__(self, request) -> None:
        # session object associated with current request
        self.session = request.session

        # get request
        self.request = request

        # get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, create a session key since it doesn't exist yet
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}  # create an empty cart and assign it to the session

        # make sure cart is available across entire application - (apps/pages)
        self.cart = cart  # Assign the retrieved or newly created cart to self.cart

    def get_cart_contents(self):
        """
        Get all cart contents to display on cart overview/summary page
        """
        # get ids from cart
        product_ids = self.cart.keys()  # cart is set up as a dictionary as defined in product template javascript and add view {product_id: quantity}
        # use these ids to look up products in DB model
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantities(self):
        """
        this method is used to get the quantity of each product in the current cart. we pass an instance of this method
        in the cart_overview view in the context dictionary, then in the cart overview page cart/overview.html, we loop
        through the passed cart to populate each dropdown menu with the current quantity of each product in the cart.
        """
        quantities = self.cart
        return quantities

    def add(self, product, quantity):
        """
        Add a product to the cart.
        """
        product_id = str(product.id)
        product_quantity = str(quantity)

        # check if the product is already in the cart
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)  # add with specified quantity
        
        self.session.modified = True

        # deal with logged-in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert cart to double-quoted product id's for json {'3':1} to {"3":1}
            cart_to_string = str(self.cart)
            converted_cart = cart_to_string.replace("\'", "\"")
            # save converted cart to Profile model
            current_user.update(old_cart=converted_cart)

    def add_from_db(self, product, quantity):
        """ A separate method to add json dict cart items back to session cart upon user logging back in"""
        product_id = str(product)
        product_quantity = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

        # deal with logged-in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert cart to double-quoted product id's for json {'3':1} to {"3":1}
            cart_to_string = str(self.cart)
            converted_cart = cart_to_string.replace("\'", "\"")
            # save converted cart to Profile model
            current_user.update(old_cart=converted_cart)

    def update(self, product, quantity):
        # shopping cart looks like: {'1': 3}, where product id is a string and quantity is an integer
        product_id = str(product)
        product_quantity = int(quantity)

        # get cart in order to update the session
        cart_to_update = self.cart

        # update cart (dictionary)
        cart_to_update[product_id] = product_quantity

        self.session.modified = True

        # let item update from cart persist upon login/logout
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert cart to double-quoted product id's for json {'3':1} to {"3":1}
            cart_to_string = str(self.cart)
            converted_cart = cart_to_string.replace("\'", "\"")
            # save converted cart to Profile model
            current_user.update(old_cart=converted_cart)

        updated_cart = self.cart
        return updated_cart

    def delete(self, product):
        product_id = str(product)

        # delete from cart
        if product_id in self.cart:
            del self.cart[product_id]
        else:
            pass

        self.session.modified = True

        # whenever user deletes from cart, it must be deleted from the DB old_cart field as well
        # let item removal from cart persist upon login/logout
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert cart to double-quoted product id's for json {'3':1} to {"3":1}
            cart_to_string = str(self.cart)
            converted_cart = cart_to_string.replace("\'", "\"")
            # save converted cart to Profile model
            current_user.update(old_cart=converted_cart)

    def calculate_total(self):
        # get product IDs and products that exist in the current cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        total = 0
        for k, v in self.cart.items():
            k = int(k)  # convert from string of id into integer in order to compare with integer pk id of DB
            for product in products:
                if k == product.id:
                    # account for if product is on sale
                    if product.is_on_sale:
                        each_item_total = product.sale_price * v
                        total += each_item_total
                    else:
                        each_item_total = product.price * v
                        total += each_item_total

        return total

    def __len__(self):
        """
            return the length of the cart, the number of distinct products in the cart
            - use for updating number in navbar cart button
        """
        return len(self.cart)
