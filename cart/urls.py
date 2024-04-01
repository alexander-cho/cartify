from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_overview, name='cart-overview'),
    path('add/', views.add_to_cart, name='add-to-cart'),
    path('delete/', views.delete_from_cart, name='delete-from-cart'),
    path('update/', views.update_cart, name='update-cart'),
]