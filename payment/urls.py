from django.urls import path
from . import views

urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('payment-success', views.payment_success, name='payment-success'),
    path('billing-info', views.billing_info, name='billing-info'),
    path('process-order', views.process_order, name='process-order'),
]