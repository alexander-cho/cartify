from django.shortcuts import render

# Create your views here.


def payment_success(request):
    return render(request, 'payment/payment_success.html')


def view_previous_orders(request):
    return '<h1>Previous Orders</h1>'


def view_recommendations(request):
    return '<h1>Recommendations</h1>'


def view_other(request):
    return '<h1>Other</h1>'