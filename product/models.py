from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Category (models.Model):
    name = models.CharField(default='',max_length=255)
class Type_Product(models.Model):
    name = models.CharField(default='',max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
class Product(models.Model):

    code = models.CharField(default='',max_length=30)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0,null=True,blank=True)
    product_image = models.ImageField(upload_to='products')
    review_article = RichTextUploadingField(default='')
    specifications = RichTextUploadingField(default='')
    special_offer = RichTextUploadingField(default='')
    name = models.CharField(default='',max_length=100)
    type = models.ForeignKey(Type_Product,on_delete=models.CASCADE)
    size = models.CharField(default='',max_length=10,null=True,blank=True)
    productUpload_at = models.DateTimeField(auto_now_add=True)
class Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_image = models.ImageField(default='',upload_to='products')
class Banner(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default='' ,null=True,blank=True)
    event = models.CharField(default='',max_length=255)
    describe = models.TextField(default='',max_length=255)
    banner_image = models.ImageField(default='', upload_to='products')
    is_show = models.BooleanField(default=False)
    discount = models.FloatField(default=0,null=True,blank=True)
