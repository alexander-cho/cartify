from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('update-password/', views.update_password, name='update-password'),
    path('product/<int:pk>/', views.product, name='product'),
    path('category/<str:c>/', views.category, name='category'),
    path('category-summary/', views.category_summary, name='category-summary'),
]