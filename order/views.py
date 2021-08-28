from django.shortcuts import render

# Create your views here.
from order.models import *
from core.views import showindex
def createOrder(request):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    name = firstname + lastname
    address = request.POST.get("address")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    cartid = request.COOKIES.get("cartid")
    cart = Cart.objects.get(pk = cartid)
    order = Order(name = name , address = address,email = email,phone = phone,cart = cart)
    listCartItem = cart.cartitem_set.all()
    order.save()
    for item in listCartItem:
        if not item.is_bought:
            orderItem = OrderItem(product = item.product , order = order , quantity = item.quantity)
            orderItem.save()
    cart.cartitem_set.filter(is_bought=False).update(is_bought = True)
    return showindex(request)
