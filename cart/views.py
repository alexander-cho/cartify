from django.shortcuts import render

# Create your views here.

def cart_overview(request):
    return render(request, 'cart/overview.html', {})


def add_to_cart(request):
    pass


def delete_from_cart(request):
    pass


def update_cart(request):
    pass