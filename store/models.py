import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Profile model to extend built in User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)  # automatically tag current time when updated
    phone_number = models.CharField(max_length=25, blank=True)
    address_one = models.CharField(max_length=50, blank=True)
    address_two = models.CharField(max_length=50, blank=True)  # ie, apt/unit/suite number
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)

    # instead of saving cart (dictionary) to database, convert it to a string
    old_cart = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username


def create_new_profile(sender: any, instance: User, created: bool, **kwargs: any) -> None:
    """
    Create a new profile associated with a user upon registration.

    Parameters:
    sender: The User class sends the signal
    instance: refers to the instance created of the data when register form is submitted
    created: indicates if a new instance of the sender class (User) was created

    Returns:
    None
    """
    if created:  # if a user has been created
        user_profile = Profile(user=instance)
        user_profile.save()


# automate signal
post_save.connect(create_new_profile, sender=User)


# customer info
class Customer(models.Model):
    """Customer model."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)  # change to PasswordField

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    """Item category model. Each product you list on your store will be in a category"""
    class Meta:
        verbose_name_plural = 'categories'  # pluralize with proper convention for admin backend display

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

        
# product info
class Product(models.Model):
    """Product model."""
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # reference Category model, if not specifically defined for item, it will default to first category you create
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')  # your uploaded product images will show up in this directory inside the media directory

    # PRODUCTS ON SALE
    is_on_sale = models.BooleanField(default=False)  # by default product your listed product will not be on sale
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self) -> str:
        return self.name
