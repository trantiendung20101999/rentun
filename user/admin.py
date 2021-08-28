from django.contrib import admin
from user.models import CustomerUser,Comment
# Register your models here.
admin.site.register(CustomerUser),
admin.site.register(Comment)