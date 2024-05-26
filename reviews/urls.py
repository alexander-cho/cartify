from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_home, name='reviews-home'),
    path('number', views.specific_review, name='specific-review'),
    path('write', views.write_review, name='write'),
]
