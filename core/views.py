import datetime

from django.shortcuts import render
from product.models import *
from user.models import *
from order.models import *


# Create your views here.
def showlogin(request):
    response = render(request, 'homepage/login.html')
    response.delete_cookie('userid')
    response.delete_cookie('checklogin')
    response.delete_cookie('role')
    return response


def showRegister(request):
    responser = render(request, 'homepage/register.html')
    return responser


def calMoneyOrder(order):
    listItem = order.orderitem_set.all()
    price = 0
    for item in listItem:
        if item.product.discount_price != 0:
            price += item.product.discount_price
        else:
            price += item.product.price
    return price
def totalMoney(order,type):
    listItem = order.orderitem_set.all()
    price = 0
    for item in listItem:
        if item.product.type.category.name == type:
            if item.product.discount_price != 0:
                price += item.product.discount_price
            else:
                price += item.product.price
    return price

def showindexAdmin(request, userid, year):
    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        date_now = datetime.datetime.now().date()
        day = datetime.datetime.now().date().day
        day = day - 1
        date_last = date_now.replace(day=day)
        listYear = []
        year_start = 2020
        while year_start <= date_now.year:
            listYear.append(year_start)
            year_start += 1
        countOrderLastDay = 0
        countOrderOnDay = 0
        countOrderUnCheck = 0
        countOrderUnShip = 0
        order_jan = 0
        order_feb = 0
        order_mar = 0
        order_apr = 0
        order_may = 0
        order_jun = 0
        order_jul = 0
        order_aug = 0
        order_sep = 0
        order_oct = 0
        order_nov = 0
        order_dec = 0
        order_elec = 0
        order_water = 0
        order_kitchen = 0
        order_fashion = 0
        order_food = 0
        listOrder = Order.objects.all()
        for order in listOrder:

            if order.ischecked == False:
                countOrderUnCheck += 1
            if order.isshipped == False:
                countOrderUnShip += 1
            if order.created_at.date() == date_now:
                countOrderOnDay += 1
            if order.created_at.date == date_last:
                countOrderLastDay += 1
            if order.created_at.year == year and order.isshipped == True:
                order_elec += totalMoney(order, "Thiết bị điện tử , điện lạnh")
                order_water += totalMoney(order, "Thiệt bị điện nước")
                order_kitchen += totalMoney(order, "Đồ gia dụng, thiết bị bếp")
                order_fashion += totalMoney(order, "Thời trang, phụ kiện thời trang")
                order_food += totalMoney(order, "Đồ ăn")
                if order.created_at.month == 1:
                    order_jan += calMoneyOrder(order)
                if order.created_at.month == 2:
                    order_feb += calMoneyOrder(order)
                if order.created_at.month == 3:
                    order_mar += calMoneyOrder(order)
                if order.created_at.month == 4:
                    order_apr += calMoneyOrder(order)
                if order.created_at.month == 5:
                    order_may += calMoneyOrder(order)
                if order.created_at.month == 6:
                    order_jun += calMoneyOrder(order)
                if order.created_at.month == 7:
                    order_jul += calMoneyOrder(order)
                if order.created_at.month == 8:
                    order_aug += calMoneyOrder(order)
                if order.created_at.month == 9:
                    order_sep += calMoneyOrder(order)
                if order.created_at.month == 10:
                    order_oct += calMoneyOrder(order)
                if order.created_at.month == 11:
                    order_nov += calMoneyOrder(order)
                if order.created_at.month == 12:
                    order_dec += calMoneyOrder(order)
        list_order_bymonth = []
        list_order_bymonth.append(order_jan)
        list_order_bymonth.append(order_feb)
        list_order_bymonth.append(order_mar)
        list_order_bymonth.append(order_apr)
        list_order_bymonth.append(order_may)
        list_order_bymonth.append(order_jun)
        list_order_bymonth.append(order_jul)
        list_order_bymonth.append(order_aug)
        list_order_bymonth.append(order_sep)
        list_order_bymonth.append(order_oct)
        list_order_bymonth.append(order_nov)
        list_order_bymonth.append(order_dec)
        context = {
            "user": user,
            "countOrderOnDay": countOrderOnDay,
            "countOrderLastDay": countOrderLastDay,
            "countOrderUnShip": countOrderUnShip,
            "countOrderUnCheck": countOrderUnCheck,
            "list_cost": list_order_bymonth,
            "year": year,
            "listYear": listYear,
            "order_elec":order_elec,
            "order_water":order_water,
            "order_kitchen":order_kitchen,
            "order_fashion":order_fashion,
            "order_food":order_food,
        }
        return render(request, 'management/index.html', context)
    else:
        response = render(request, 'homepage/login.html')
        return response


def showindex(request):
    cartid = request.COOKIES.get('cartid')
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    if cartid != None:
        cartt = Cart.objects.filter(pk=cartid)
        if cartt.count() == 0:
            cart = Cart()
            cart.save()
        else :
            cart = cartt[0]
    else:
        cart = Cart()
        cart.save()

    listCartItem = cart.cartitem_set.filter(is_bought=False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    listCate = Category.objects.all()
    listTypee = Type_Product.objects.all()
    listBanner = Banner.objects.filter(is_show=True)
    category = Category.objects.get(pk=2)
    listType = category.type_product_set.all()
    listCold = []
    listCold_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listCold.append(product)
    listCold.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listCold:
        if count < 6:
            count += 1
            listCold_public.append(item)
        else:
            break
    category = Category.objects.get(pk=3)
    listType = category.type_product_set.all()
    listWater = []
    listWater_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listWater.append(product)
    listWater.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listWater:
        if count < 6:
            count += 1
            listWater_public.append(item)
        else:
            break
    category = Category.objects.get(pk=4)
    listType = category.type_product_set.all()
    listKitchen = []
    listKitchen_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listKitchen.append(product)
    listKitchen.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listKitchen:
        if count < 6:
            count += 1
            listKitchen_public.append(item)
        else:
            break
    category = Category.objects.get(pk=5)
    listType = category.type_product_set.all()
    listFashion = []
    listFashion_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listFashion.append(product)
    listFashion.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listFashion:
        if count < 6:
            count += 1
            listFashion_public.append(item)
        else:
            break
    category = Category.objects.get(pk=6)
    listType = category.type_product_set.all()
    listFood = []
    listFood_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listFood.append(product)
    listFood.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listFood:
        if count < 6:
            count += 1
            listFood_public.append(item)
        else:
            break
    context = {
        "listCold": listCold_public,
        "listWater": listWater_public,
        "listKitchen": listKitchen_public,
        "listFashion": listFashion_public,
        "listFood": listFood_public,
        "listCate": listCate,
        "listType": listTypee,
        "listBanner": listBanner,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "user": user
    }
    response = render(request, 'homepage/index.html', context)
    response.set_cookie('cartid', cart.id)
    return response


def showContact(request):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought=False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    listCate = Category.objects.all()
    listTypee = Type_Product.objects.all()
    listBanner = Banner.objects.filter(is_show=True)
    category = Category.objects.get(pk=2)
    listType = category.type_product_set.all()
    listCold = []
    listCold_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listCold.append(product)
    listCold.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listCold:
        if count < 6:
            count += 1
            listCold_public.append(item)
        else:
            break
    category = Category.objects.get(pk=3)
    listType = category.type_product_set.all()
    listWater = []
    listWater_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listWater.append(product)
    listWater.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listWater:
        if count < 6:
            count += 1
            listWater_public.append(item)
        else:
            break
    category = Category.objects.get(pk=4)
    listType = category.type_product_set.all()
    listKitchen = []
    listKitchen_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listKitchen.append(product)
    listKitchen.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listKitchen:
        if count < 6:
            count += 1
            listKitchen_public.append(item)
        else:
            break
    category = Category.objects.get(pk=5)
    listType = category.type_product_set.all()
    listFashion = []
    listFashion_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listFashion.append(product)
    listFashion.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listFashion:
        if count < 6:
            count += 1
            listFashion_public.append(item)
        else:
            break
    category = Category.objects.get(pk=6)
    listType = category.type_product_set.all()
    listFood = []
    listFood_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listFood.append(product)
    listFood.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listFood:
        if count < 6:
            count += 1
            listFood_public.append(item)
        else:
            break
    context = {
        "listCold": listCold_public,
        "listWater": listWater_public,
        "listKitchen": listKitchen_public,
        "listFashion": listFashion_public,
        "listFood": listFood_public,
        "listCate": listCate,
        "listType": listTypee,
        "listBanner": listBanner,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "user": user
    }
    response = render(request, 'homepage/contact.html', context)
    return response


def showCart(request):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought=False)
    listCartItemDone = cart.cartitem_set.filter(is_bought=True)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    listCate = Category.objects.all()
    listTypee = Type_Product.objects.all()
    listBanner = Banner.objects.filter(is_show=True)
    category = Category.objects.get(pk=2)
    listType = category.type_product_set.all()
    listCold = []
    listCold_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listCold.append(product)
    listCold.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listCold:
        if count < 6:
            count += 1
            listCold_public.append(item)
        else:
            break
    category = Category.objects.get(pk=3)
    listType = category.type_product_set.all()
    listWater = []
    listWater_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listWater.append(product)
    listWater.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listWater:
        if count < 6:
            count += 1
            listWater_public.append(item)
        else:
            break
    category = Category.objects.get(pk=4)
    listType = category.type_product_set.all()
    listKitchen = []
    listKitchen_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listKitchen.append(product)
    listKitchen.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listKitchen:
        if count < 6:
            count += 1
            listKitchen_public.append(item)
        else:
            break
    category = Category.objects.get(pk=5)
    listType = category.type_product_set.all()
    listFashion = []
    listFashion_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listFashion.append(product)
    listFashion.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listFashion:
        if count < 6:
            count += 1
            listFashion_public.append(item)
        else:
            break
    category = Category.objects.get(pk=6)
    listType = category.type_product_set.all()
    listFood = []
    listFood_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listFood.append(product)
    listFood.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listFood:
        if count < 6:
            count += 1
            listFood_public.append(item)
        else:
            break
    context = {
        "listCold": listCold_public,
        "listWater": listWater_public,
        "listKitchen": listKitchen_public,
        "listFashion": listFashion_public,
        "listFood": listFood_public,
        "listCate": listCate,
        "listType": listTypee,
        "listBanner": listBanner,
        "listCartItem": listCartItem,
        "listCartItemDone": listCartItemDone,
        "cart": cart,
        "total": total,
        "user": user
    }
    response = render(request, 'homepage/cart.html', context)
    return response


def showCheckout(request):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought=False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    listCate = Category.objects.all()
    listTypee = Type_Product.objects.all()
    listBanner = Banner.objects.filter(is_show=True)
    category = Category.objects.get(pk=2)
    listType = category.type_product_set.all()
    listCold = []
    listCold_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listCold.append(product)
    listCold.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listCold:
        if count < 6:
            count += 1
            listCold_public.append(item)
        else:
            break
    category = Category.objects.get(pk=3)
    listType = category.type_product_set.all()
    listWater = []
    listWater_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listWater.append(product)
    listWater.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listWater:
        if count < 6:
            count += 1
            listWater_public.append(item)
        else:
            break
    category = Category.objects.get(pk=4)
    listType = category.type_product_set.all()
    listKitchen = []
    listKitchen_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listKitchen.append(product)
    listKitchen.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listKitchen:
        if count < 6:
            count += 1
            listKitchen_public.append(item)
        else:
            break
    category = Category.objects.get(pk=5)
    listType = category.type_product_set.all()
    listFashion = []
    listFashion_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listFashion.append(product)
    listFashion.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listFashion:
        if count < 6:
            count += 1
            listFashion_public.append(item)
        else:
            break
    category = Category.objects.get(pk=6)
    listType = category.type_product_set.all()
    listFood = []
    listFood_public = []
    for type in listType:
        list_Product = type.product_set.all()
        for product in list_Product:
            listFood.append(product)
    listFood.sort(key=lambda x: x.productUpload_at, reverse=True)
    count = 0
    for item in listFood:
        if count < 6:
            count += 1
            listFood_public.append(item)
        else:
            break
    context = {
        "listCold": listCold_public,
        "listWater": listWater_public,
        "listKitchen": listKitchen_public,
        "listFashion": listFashion_public,
        "listFood": listFood_public,
        "listCate": listCate,
        "listType": listTypee,
        "listBanner": listBanner,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "user": user
    }
    response = render(request, 'homepage/checkout.html', context)
    return response
