from django.contrib import admin
from product.models import Product,Image,Category,Type_Product,Banner
# Register your models here.
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Type_Product)
admin.site.register(Banner)
