from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Customer, Product, Profile

# Register from models.py
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Profile)


# mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile


# extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]  # include everything in the Profile model inside each User for the admin area


# unregister old format
admin.site.unregister(User)

# re-register
admin.site.register(User, UserAdmin)
