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
app_name="product"
from . import views
urlpatterns = [
    # path('checklogin/', views.checklogin, name="checklogin"),
    # path('add_product/<int:userid>/',views.show_addProduct,name="add_product")
    path('add_category/<int:userid>/',views.addCategory,name="add_category"),
    path('add_type/<int:userid>/',views.addType,name="add_type"),
    path('search_product/<int:userid>/',views.searchProduct,name="search_product"),
    path('search_product2/<int:userid>/', views.searchProduct2, name="search_product2"),
    path('addToCart/<int:quantity>/',views.addToCart,name="addToCart"),
    path('delFromCart/',views.delFromCart,name="delFromCart"),
    path('showProduct/<int:productid>/',views.showProduct,name="showProduct"),
    path('searchByName/<int:start>/', views.searchProductByName, name="searchByName"),
    path('showAllProduct/<int:start>/', views.showAllProduct, name="showAllProduct"),
    path('showProductByCate/<int:categoryid>/<int:start>/', views.showProductByCategory, name="showProductByCate"),
    path('showProductByType/<int:typeid>/<int:start>/', views.showProductByType, name="showProductByType"),
    path('filterAllProduct/<int:minn>/<int:maxx>/<int:start>/', views.filterAllProduct, name="filterAllProduct"),
    path('filterProductByCate/<int:categoryid>/<int:minn>/<int:maxx>/<int:start>/', views.filterProductByCategory, name="filterProductByCate"),
    path('filterProductByType/<int:typeid>/<int:minn>/<int:maxx>/<int:start>/', views.filterProductByType, name="filterProductByType"),
    path('sortAllProduct/<int:sort>/<int:start>/', views.sortAllProduct, name="sortAllProduct"),
    path('sortProductByCate/<int:sort>/<int:categoryid>/<int:start>/', views.sortProductByCategory, name="sortProductByCate"),
    path('sortProductByType/<int:sort>/<int:typeid>/<int:start>/', views.sortProductByType, name="sortProductByType"),
]
