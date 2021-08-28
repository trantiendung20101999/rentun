from django.db import models
from user.models import CustomerUser
from product.models import Product
# Create your models here.
class Cart (models.Model):
    user = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    ischecked = models.BooleanField(default=False)
    isshipped = models.BooleanField(default=False)
    address = models.CharField(default='',max_length=255)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,default='')
    name = models.CharField(default='',max_length=255)
    phone = models.CharField(default='',max_length=255)
    email = models.CharField(default='',max_length=255)
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,default='')
    quantity = models.IntegerField(default=0)
    is_bought = models.BooleanField(default=False)
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default='')
    quantity = models.IntegerField(default=0)

