from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class ClothingType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ClothingSize(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SearchType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    topic = models.ForeignKey(ClothingType, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    size = models.ForeignKey(ClothingSize, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(default="placeholder.png", null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.item_name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_tax(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems]) * .0825
        return total

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        tax = sum([item.get_total for item in orderItems]) * .0825
        total = sum([item.get_total for item in orderItems]) + tax
        return total

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address