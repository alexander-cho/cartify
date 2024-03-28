from django.db import models
import datetime

# Create your models here.

# categories of products
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


# customer info
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

        
# product info
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    # On sale products
    is_on_sale = models.BooleanField(default=False) # by default product is not on sale
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self) -> str:
        return self.name
    

# order and shipping info
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    shipping_address = models.CharField(max_length=100, default='', blank=True)
    phone_number = models.CharField(max_length=20, default='', blank=True)
    date_ordered = models.DateField(default=datetime.datetime.today)
    shipping_status = models.BooleanField(default=False) # false because when customer first order it's not been shipped yet

    def __str__(self) -> str:
        return self.product