"""shopp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
app_name="users"
from . import views
urlpatterns = [
    path('checklogin/', views.checklogin, name="checklogin"),
    path('add_product/<int:userid>/',views.show_addProduct,name="add_product"),
    path('add_image/<int:userid>/',views.show_addImage,name="add_image"),
    path('add_image2/<int:userid>/<int:productid>', views.add_image, name="add_image2"),
    path('add_banner/<int:userid>/', views.show_addBanner, name="add_banner"),
    path('update_product/<int:userid>',views.update_product,name="update_product"),
    path('update_product2/<int:userid>/<int:productid>', views.update_product2, name="update_product2"),
    path('update_banner/<int:userid>',views.update_banner,name="update_banner"),
    path('check_order/<int:userid>', views.check_order, name="check_order"),
    path('check_order2/<int:userid>/<int:orderid>', views.check_order2, name="check_order2"),
    path('ship_order/<int:userid>/<int:orderid>', views.ship_order, name="ship_order"),
    path('detail_order/<int:userid>/<int:orderid>', views.detail_order, name="detail_order"),
    path('update_banner2/<int:userid>/<int:productid>', views.update_banner2, name="update_banner2"),
    path('register/', views.register, name="register"),
    path('addComment/<int:productid>', views.add_comment, name="add_comment"),

]
