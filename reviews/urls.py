from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews_home, name='reviews-home'),
    path('<int:pk>', views.specific_review, name='specific-review'),
    path('write', views.write_review, name='write-review'),
    path('<int:pk>/edit', views.edit_review, name='edit-review'),
    path('<int:pk>/delete', views.delete_review, name='delete-review'),
    path('<int:pk>/delete-confirm', views.confirm_delete_review, name='delete-review-confirm'),
]
