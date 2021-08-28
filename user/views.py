import datetime
import sys
import traceback

from django.http import HttpResponse
from django.shortcuts import render
from user.models import CustomerUser,Comment
from product.forms import PostForm,PostFormUpdate,BannerForm,BannerFormUpdate,ImageForm
from product.models import *
from core.views import showindex,showlogin,showindexAdmin
from product.views import showProduct
from order.models import *
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login


# def register(request):
#     username = request.POST.get("username")
#     password = request.POST.get("password")
#     repassword = request.POST.get("repassword")
#
#     if CustomerUser.objects.filter(username = username).exists() is False:
#         user = CustomerUser.objects.create_user(username=username, password=password)
#         user.save()
#         context = {"warning": "Đăng ký thành công"}
#         return render(request,'homepage/login.html',context)
#     elif(password != repassword):
#         context = {"warning": "Nhập lại mật khẩu không chính xác"}
#     else:
#         context = {"warning": "Tài khoản đã tồn tại "}
#
#     return render(request, 'homepage/register.html', context)

def checklogin(request):
    if request.method =="POST":
        username=request.POST.get("username")
        password = request.POST.get("password")
        myuser = authenticate(username=username, password = password)
        context = {"warning": "Tài khoản hoặc mật khẩu không chính xác"}
        if(myuser != None):
            if(myuser.discriminator == "admin"):
                date_now = datetime.datetime.now().date()
                response = showindexAdmin(request,myuser.id,date_now.year)
                response.set_cookie('checklogin', myuser.password)
                response.set_cookie('role','admin')
                return response
            if (myuser.discriminator == "customer"):
                cartid = request.COOKIES.get('cartid')
                user = "true"
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
                response = render(request, 'homepage/index.html', context)
                response.set_cookie('cartid', cart.id)
                response.set_cookie('userid',myuser.id)
                return response
        response = render(request,'homepage/login.html',context)
        return response
    else:
        context = {"warning": "Tài khoản hoặc mật khẩu không chính xác"}
        response = render(request, 'homepage/login.html',context)
        return response
    # if myuser is None:
    #     return render(request,'homepage/login.html',context)
    # login(request,myuser)
    # return call(myuser,request)
def add_image(request,userid,productid):
    date_now = datetime.datetime.now().date()
    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES)
            product = Product.objects.get(pk = productid)
            if form.is_valid():
                post_item = form.save(commit=False)
                post_item.product = product
                post_item.save()
                form = ImageForm()
                listProduct = Product.objects.all()
                context = {
                    "userid": userid,
                    "form": form,
                    "listProduct": listProduct,
                    "year": date_now.year
                }
                return render(request, 'management/add_image.html', context)
            else:
                return HttpResponse(form.errors)
        else:
            form = ImageForm()
            product = Product.objects.get(pk = productid)
            context = {"form": form,
                       "product":product,
                       "userid": userid
                       }
            response = render(request, 'management/add_image.html', context)
            return response
    else:
        response = render(request, 'homepage/login.html')
        return response
def show_addImage(request,userid):
    date_now = datetime.datetime.now().date()
    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        listProduct = Product.objects.all().order_by('-productUpload_at')
        context = {
            "userid": userid,
            "listProduct": listProduct,
            "year":date_now.year
        }
        return render(request, 'management/add_image.html', context)
    else:
        response = render(request, 'homepage/login.html')
        return response
def show_addBanner(request,userid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        if request.method == "POST":
            form = BannerForm(request.POST, request.FILES)
            cateid = request.POST.get("cate")
            cate = Category.objects.get(pk=cateid)
            if form.is_valid():
                post_item = form.save(commit=False)
                post_item.category = cate
                post_item.save()
                form = BannerForm()
                listCate = Category.objects.all()
                context = {
                    "userid": userid,
                    "form": form,
                    "listCate": listCate,
                    "year":date_now.year
                }
                return render(request, 'management/add_banner.html', context)
            else:
                return HttpResponse(form.errors)
        else:
            form = BannerForm()
            listCate = Category.objects.all()
            context={"form":form,
                     "listCate":listCate,
                     "userid":userid,
                     "year":date_now.year
                     }
            response = render(request,'management/add_banner.html',context)
            return response
    else:
        response = render(request, 'homepage/login.html')
        return response
def show_addProduct(request,userid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            code = request.POST.get("code")
            name = request.POST.get("name")
            price = request.POST.get("price")
            price_discount = request.POST.get("discount_price")
            quantity = request.POST.get("quantity")
            size = request.POST.get("size")
            typeid = request.POST.get("type")
            typee = Type_Product.objects.get(pk=typeid)
            if form.is_valid() :
                post_item = form.save(commit=False)
                post_item.code = code
                post_item.price = price
                post_item.discount_price = price_discount
                post_item.quantity = quantity
                post_item.size = size
                post_item.price_quantity = price_discount
                post_item.type = typee
                post_item.name = name
                post_item.save()
                form = PostForm()
                listCate = Category.objects.all()
                listType = Type_Product.objects.all()
                context = {
                    "userid": userid,
                    "form": form,
                    "listCate": listCate,
                    "listType": listType,
                    "year":date_now.year}
                return render(request,'management/add_product.html',context)

            else:
                return HttpResponse("Hãy điền đủ thông tin cần thiết của sản phẩm ")
        else:
            form = PostForm()
            listCate = Category.objects.all()
            listType = Type_Product.objects.all()
            context={
                    "userid":userid,
                    "form":form,
                    "listCate":listCate,
                     "listType":listType,
                    "year":date_now.year}

            return render(request,'management/add_product.html',context)
    else :
        response = render(request, 'homepage/login.html')
        return response
def update_banner(request,userid):
    date_now = datetime.datetime.now().date()
    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        listBanner = Banner.objects.all().order_by('-is_show')
        context = {
            "userid": userid,
            "listBanner": listBanner,
            "year":date_now.year
        }
        return render(request, 'management/update_banner.html', context)
    else:
        response = render(request, 'homepage/login.html')
        return response
def check_order(request,userid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        listOrder = Order.objects.all().order_by('ischecked','isshipped')
        context = {
            "userid": userid,
            "listOrder": listOrder,
            "year":date_now.year
        }
        return render(request, 'management/check_order.html', context)
    else:
        response = render(request, 'homepage/login.html')
        return response
def check_order2(request,userid,orderid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        Order.objects.filter(id = orderid).update(ischecked = True)
        listOrder = Order.objects.all().order_by('ischecked', 'isshipped')
        context = {
            "userid": userid,
            "listOrder": listOrder,
            "year":date_now.year
        }
        return render(request, 'management/check_order.html', context)
    else:
        response = render(request, 'homepage/login.html')
        return response
def ship_order(request,userid,orderid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        Order.objects.filter(id = orderid).update(isshipped = True)
        listOrder = Order.objects.all().order_by('ischecked', 'isshipped')
        context = {
            "userid": userid,
            "listOrder": listOrder,
            "year":date_now.year
        }
        return render(request, 'management/check_order.html', context)
    else:
        response = render(request, 'homepage/login.html')
        return response
def detail_order(request,userid,orderid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    order = Order.objects.get(pk = orderid)
    listCartItem = order.orderitem_set.all()
    price = 0
    for item in listCartItem:
        if item.product.discount_price != 0 :
            price += item.product.discount_price
        else:
            price += item.product.price
    context = {
        "userid": userid,
        "order": order,
        "listCartItem":listCartItem,
        "total": price,
        "year":date_now.year
    }
    return render(request, 'management/check_order.html', context)
def update_banner2(request,userid,productid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        if request.method == "POST":
            form = BannerFormUpdate(request.POST, request.FILES)
            cateid = request.POST.get("cate")
            cate = Category.objects.get(pk=cateid)
            if form.is_valid():
                post_item = form.save(commit=False)
                post_item.category = cate
                Banner.objects.filter(id=productid).update( category = cate,
                                                            event = post_item.event,
                                                            describe = post_item.describe,
                                                            is_show = post_item.is_show,
                                                            discount = post_item.discount
                                                            )
                banner = Banner.objects.get(pk=productid)
                listBanner = Banner.objects.all().order_by('-is_show')
                form = BannerFormUpdate(instance=banner)
                listCate = Category.objects.all()
                listType = Type_Product.objects.all()
                context = {
                    "listBanner":listBanner,
                    "userid": userid,
                    "form": form,
                    "listCate": listCate,
                    "year":date_now.year,
                    "listType": listType}
                return render(request, 'management/update_banner.html', context)

            else:
                return HttpResponse(form.errors)
        else:
            listCate = Category.objects.all()
            listType = Type_Product.objects.all()
            banner = Banner.objects.get(pk=productid)
            form = BannerFormUpdate(instance=banner)
            context = {
                "product": banner,
                "userid": userid,
                "form": form,
                "listCate": listCate,
                "listType": listType,
                "year":date_now.year,
            }

            return render(request, 'management/update_banner.html', context)
    else:
        response = render(request, 'homepage/login.html')
        return response
def update_product(request,userid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        listProduct = Product.objects.all()
        context = {
            "userid": userid,
            "listProduct":listProduct,
            "year":date_now.year
                }
        return render(request, 'management/update_product.html', context)
    else :
        response = render(request, 'homepage/login.html')
        return response
def update_product2(request,userid,productid):
    date_now = datetime.datetime.now().date()

    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        if request.method == "POST":
            form = PostFormUpdate(request.POST, request.FILES)
            code = request.POST.get("code")
            name = request.POST.get("name")
            price = request.POST.get("price")
            price_discount = request.POST.get("discount_price")
            quantity = request.POST.get("quantity")
            size = request.POST.get("size")
            typeid = request.POST.get("type")
            typee = Type_Product.objects.get(pk=typeid)
            if form.is_valid():
                post_item = form.save(commit=False)
                post_item.code = code
                post_item.price = price
                post_item.quantity = quantity
                post_item.size = size
                post_item.price_quantity = price_discount
                post_item.type = typee
                post_item.name = name
                Product.objects.filter(id = productid).update(code = code , price = price,quantity =quantity,
                                                              size = size , discount_price = price_discount,
                                                              type = typee , name = name ,
                                                              review_article = post_item.review_article,
                                                              specifications = post_item.specifications,
                                                              special_offer = post_item.special_offer
                                                              )
                product = Product.objects.get(pk=productid)
                form = PostFormUpdate(instance= product)
                listCate = Category.objects.all()
                listType = Type_Product.objects.all()
                context = {
                    "product":product,
                    "userid": userid,
                    "form": form,
                    "listCate": listCate,
                    "year":date_now.year,
                    "listType": listType}
                return render(request, 'management/update_product.html', context)

            else:
                return HttpResponse(form.errors)
        else:
            listCate = Category.objects.all()
            listType = Type_Product.objects.all()
            product = Product.objects.get(pk=productid)
            form = PostFormUpdate(instance = product)
            context = {
                "product":product,
                "userid": userid,
                "form":form,
                "listCate": listCate,
                "listType": listType,
                "year":date_now.year
                    }

            return render(request, 'management/update_product.html', context)
    else :
        response = render(request, 'homepage/login.html')
        return response

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    repassword = request.POST.get("repassword")

    if CustomerUser.objects.filter(username=username).exists() is False:
        user = CustomerUser.objects.create_user(username=username, password=password,discriminator='customer')
        user.save()
        context = {"warning": "Đăng ký thành công"}
        return render(request, 'homepage/login.html', context)
    elif (password != repassword):
        context = {"warning": "Nhập lại mật khẩu không chính xác"}
    else:
        context = {"warning": "Tài khoản đã tồn tại "}

    return render(request, 'homepage/register.html', context)
def add_comment(request,productid):
    userid = request.COOKIES.get("userid")
    if userid != None:
        user = CustomerUser.objects.get(pk=userid)
        product = Product.objects.get(pk = productid)
        content = request.POST.get("content")
        comment = Comment(user = user,product=product,content=content)
        comment.save()
        return showProduct(request, productid)
    else:
        return showlogin(request)
