from store.models import Product


class Cart:
    def __init__(self, request) -> None:
        # session object associated with current request
        self.session = request.session

        # get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, create a session key since it doesn't exist yet
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available across entire application - (apps/pages)
        self.cart = cart

    def get_cart(self):
        # get ids from cart
        product_ids = self.cart.keys()  # set up as dictionary as defined in product template jquery and add view {product_id: price}
        # use ids to look up products in DB model
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantities(self):
        quantities = self.cart
        return quantities

    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)
        
        self.session.modified = True

    def update(self, product, quantity):
        # shopping cart looks like: {'1': 3}, where product id is a string and quantity is an integer
        product_id = str(product)
        product_quantity = int(quantity)

        # get cart in order to update the session
        cart_to_update = self.cart

        # update cart (dictionary)
        cart_to_update[product_id] = product_quantity

        self.session.modified = True

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

    '''
    return the length of the cart
    '''
    def __len__(self):
        return len(self.cart)
    