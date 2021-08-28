from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from product.models import Product
class CustomerUser(AbstractUser):
    phone_number = models.CharField(default='',max_length=15,null=True)
    address = models.CharField(default='',max_length=255,null=True)
    discriminator = models.CharField(default='',max_length=255)
class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    content = models.TextField(default='',max_length=255)
