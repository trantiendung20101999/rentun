from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from product.forms import PostForm
from product.models import *
from order.models import *
from user.models import *
# Create your views here.
def addCategory(request,userid):
    if request.method == "POST":
        name = request.POST.get("name")
        category = Category(name=name)
        category.save()
        form = PostForm()
        listCate = Category.objects.all()
        listType = Type_Product.objects.all()
        context = {
                    "userid":userid,
                    "form": form,
                   "listCate": listCate,
                   "listType": listType}

        return render(request, 'management/add_product.html', context)
def addType(request,userid):
    if request.method == "POST":
        name = request.POST.get("name")
        cateid = request.POST.get("cateid")
        category = Category.objects.get(pk=cateid)
        type = Type_Product(name = name, category = category)
        type.save()
        form = PostForm()
        listCate = Category.objects.all()
        listType = Type_Product.objects.all()
        context = {
                    "userid":userid,
                    "form": form,
                   "listCate": listCate,
                   "listType": listType}

        return render(request, 'management/add_product.html', context)
def searchProduct(request,userid):
    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        productCode = str(request.POST.get('code'))
        listProduct = Product.objects.filter(code__icontains = productCode)
        context = {
            "userid": userid,
            "listProduct": listProduct,
        }
        return render(request, 'management/update_product.html', context)
    else:
        return render(request,'homepage/login.html')
def searchProduct2(request,userid):
    user = CustomerUser.objects.get(pk=userid)
    if request.COOKIES.get('checklogin') == user.password and request.COOKIES.get('role') == 'admin':
        productCode = str(request.POST.get('code'))
        listProduct = Product.objects.filter(code__icontains=productCode)
        context = {
            "userid": userid,
            "listProduct": listProduct,
        }
        return render(request, 'management/add_image.html', context)
    else:
        return render(request, 'homepage/login.html')
def searchProductByName(request,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    name = request.POST.get("name")
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    listAllProduct = Product.objects.filter(name__icontains = name).order_by('-productUpload_at')
    listProduct = []
    inrange = range(start, start + 9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if (product.discount_price == 0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < listAllProduct.count():
            listProduct.append(listAllProduct[i])
        else:
            break
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
    context = {
        "listCate": listAllCate,
        "listType": listAllType,
        "listProduct": listProduct,
        "start": (start + 9),
        "min": min,
        "max": max,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "status": "name",
        "user": user
    }
    return render(request, "homepage/shop.html", context)
def addToCart(request,quantity):
    if request.is_ajax:
        productid = request.GET.get('productid')
        product = Product.objects.get(pk=productid)
        cartid = request.GET.get('cartid')
        quantity = int(request.GET.get('quantity'))
        cart = Cart.objects.get(pk = cartid)
        listCartItem = cart.cartitem_set.filter(is_bought=False)
        check = False
        for cartitem in listCartItem:
            if cartitem.product.id == product.id:
                CartItem.objects.filter(pk= cartitem.id).update(quantity = cartitem.quantity +quantity)
                check=True
        if check == False :
            cartitem = CartItem(product = product,cart = cart , quantity = 1 )
            cartitem.save()
        listCartItem = cart.cartitem_set.filter(is_bought=False)
        listProduct =[]
        for cartitem in listCartItem:
            listProduct.append(cartitem.product)
        qs_json = serializers.serialize('json', listProduct)
        qs_json2 = serializers.serialize('json', listCartItem)
        return JsonResponse({"listProduct": qs_json,"listCartItem":qs_json2}, status=200)
    return HttpResponse("Hãy điền đủ thông tin cần thiết của sản phẩm ")
def delFromCart(request):
    if request.is_ajax:
        productid = request.GET.get('productid')
        product = Product.objects.get(pk=productid)
        cartid = request.GET.get('cartid')
        cart = Cart.objects.get(pk = cartid)
        listCartItem = cart.cartitem_set.filter(is_bought=False)
        for cartitem in listCartItem:
            if cartitem.product.id == product.id:
                CartItem.objects.get(pk= cartitem.id).delete()
        listCartItem = cart.cartitem_set.filter(is_bought=False)
        listProduct =[]
        for cartitem in listCartItem:
            listProduct.append(cartitem.product)
        qs_json = serializers.serialize('json', listProduct)
        qs_json2 = serializers.serialize('json', listCartItem)
        return JsonResponse({"listProduct": qs_json,"listCartItem":qs_json2}, status=200)
    return HttpResponse("Hãy điền đủ thông tin cần thiết của sản phẩm ")
def showProduct(request,productid):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    listCate = Category.objects.all()
    listType = Type_Product.objects.all()
    product = Product.objects.get(pk=productid)
    listComment = Comment.objects.filter(product = product)
    cartid = request.COOKIES.get('cartid')
    listImage = product.image_set.all()
    cart = Cart.objects.get(pk =cartid)
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    listProduct  = Product.objects.all()
    listRelated =[]
    listTypeRelated = product.type.category.type_product_set.all()

    for type in listTypeRelated:
        listRelatedCate = type.product_set.all()
        for item in listRelatedCate:
            if item.id != product.id:
                listRelated.append(item)
    min = 100000000
    max =0
    for item in listProduct:
        if item.price > max :
            max = item.price
        if item.price < min :
            min = item.price
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context = {"listCate":listCate,
               "listType":listType,
               "product":product,
               "listComment":listComment,
               "cart":cart,
               "listCartItem":listCartItem,
               "total":total,
               "max":max,
               "min":min,
               "listRelated":listRelated,
               "listImage":listImage,
               "user":user}
    response = render(request,"homepage/product.html",context)
    return response
def showAllProduct(request,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    listAllProduct = Product.objects.order_by('-productUpload_at')
    listProduct = []
    inrange = range(start,start+9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if(product.discount_price ==0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < listAllProduct.count():
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context ={
        "listCate":listAllCate,
        "listType":listAllType,
        "listProduct":listProduct,
        "start": (start+9),
        "min": min,
        "max": max,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "status":"all",
        "user":user
    }
    return render(request,"homepage/shop.html",context)
def showProductByCategory(request,categoryid,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    category = Category.objects.get(pk = categoryid)
    listType = category.type_product_set.all()
    listAllProduct = []
    for type in listType:
        Products = type.product_set.all()
        for product in Products:
            listAllProduct.append(product)
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    listProduct = []
    inrange = range(start, start + 9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if (product.discount_price == 0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < len(listAllProduct):
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context = {
        "listCate": listAllCate,
        "listType": listAllType,
        "listProduct": listProduct,
        "start": (start + 9),
        "min": min,
        "max": max,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "status": "category",
        "category":category,
        "user":user
    }
    return render(request, "homepage/shop.html", context)
def showProductByType(request,typeid,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    type = Type_Product.objects.get(pk = typeid)
    listAllProduct = type.product_set.all()
    listProduct = []
    inrange = range(start, start + 9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if (product.discount_price == 0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < listAllProduct.count():
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context = {
        "listCate": listAllCate,
        "listType": listAllType,
        "listProduct": listProduct,
        "start": (start + 9),
        "min": min,
        "max": max,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "status": "type",
        "type":type,
        "user":user
    }
    return render(request, "homepage/shop.html", context)
def filterAllProduct(request,minn,maxx,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    if request.method == "POST":
        minn = request.POST.get("min")
        maxx = request.POST.get("max")
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    listAllProduct = Product.objects.filter(price__range = (minn,maxx))
    # .filter(price__range=(min_price, max_price))
    listProduct = []
    inrange = range(start, start + 9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if (product.discount_price == 0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < listAllProduct.count():
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context = {
        "listCate": listAllCate,
        "listType": listAllType,
        "listProduct": listProduct,
        "start": (start + 9),
        "min": min,
        "max": max,
        "minn":minn,
        "maxx":maxx,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "status": "filterall",
        "user":user
    }
    return render(request, "homepage/shop.html", context)
def filterProductByCategory(request,categoryid,minn,maxx,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    if request.method == "POST":
        minn = request.POST.get("min")
        maxx = request.POST.get("max")
    category = Category.objects.get(pk=categoryid)
    listType = category.type_product_set.all()
    listAllProduct = []
    for type in listType:
        Products = type.product_set.filter(price__range = (minn,maxx))
        for product in Products:
            listAllProduct.append(product)
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    listProduct = []
    inrange = range(start, start + 9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if (product.discount_price == 0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < len(listAllProduct):
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context = {
        "listCate": listAllCate,
        "listType": listAllType,
        "listProduct": listProduct,
        "start": (start + 9),
        "min": min,
        "max": max,
        "minn":minn,
        "maxx":maxx,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "status": "filtercategory",
        "category": category,
        "user":user
    }
    return render(request, "homepage/shop.html", context)
def filterProductByType(request,typeid,minn,maxx,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    if request.method == "POST":
        minn = request.POST.get("min")
        maxx = request.POST.get("max")
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    type = Type_Product.objects.get(pk=typeid)
    listAllProduct = type.product_set.filter(price__range = (minn,maxx))
    listProduct = []
    inrange = range(start, start + 9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if (product.discount_price == 0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < listAllProduct.count():
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context = {
        "listCate": listAllCate,
        "listType": listAllType,
        "listProduct": listProduct,
        "start": (start + 9),
        "min": min,
        "max": max,
        "minn":minn,
        "maxx":maxx,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "status": "filtertype",
        "type": type,
        "user":user
    }
    return render(request, "homepage/shop.html", context)
def sortAllProduct(request,sort,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    if request.method == "POST":
        sort = int(request.POST.get("sorting"))
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    if sort == 0 :
        listAllProduct = Product.objects.order_by('-productUpload_at')
    if sort == 1 :
        listAllProduct = Product.objects.order_by('-price')
    if sort == 2 :
        listAllProduct = Product.objects.order_by('price')
    listProduct = []
    inrange = range(start,start+9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if(product.discount_price ==0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < listAllProduct.count():
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context ={
        "listCate":listAllCate,
        "listType":listAllType,
        "listProduct":listProduct,
        "start": (start+9),
        "min": min,
        "max": max,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "sort":sort,
        "status":"sortall",
        "user":user
    }
    return render(request,"homepage/shop.html",context)
def sortProductByCategory(request,sort,categoryid,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    if request.method == "POST":
        sort = int(request.POST.get("sorting"))
    category = Category.objects.get(pk = categoryid)
    listType = category.type_product_set.all()
    listAllProduct = []
    for type in listType:
        Products = type.product_set.all()
        for product in Products:
            listAllProduct.append(product)
    if sort == 0:
        listAllProduct.sort(key=lambda x: x.productUpload_at, reverse=True)
    if sort == 1:
        listAllProduct.sort(key=lambda x: x.price, reverse=True)
    if sort == 2:
        listAllProduct.sort(key=lambda x: x.price, reverse=False)
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    listProduct = []
    inrange = range(start, start + 9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if (product.discount_price == 0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < len(listAllProduct):
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context = {
        "listCate": listAllCate,
        "listType": listAllType,
        "listProduct": listProduct,
        "start": (start + 9),
        "min": min,
        "max": max,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "sort":sort,
        "status": "sortcategory",
        "category":category,
        "user":user
    }
    return render(request, "homepage/shop.html", context)
def sortProductByType(request,sort,typeid,start):
    userid = request.COOKIES.get('userid')
    if userid != None:
        user = "true"
    else:
        user = "false"
    if request.method == "POST":
        sort = int(request.POST.get("sorting"))
    listAllCate = Category.objects.all()
    listAllType = Type_Product.objects.all()
    type = Type_Product.objects.get(pk = typeid)
    if sort == 0:
        listAllProduct = type.product_set.order_by('-productUpload_at')
    if sort == 1:
        listAllProduct = type.product_set.order_by('-price')
    if sort == 2:
        listAllProduct = type.product_set.order_by('price')
    listProduct = []
    inrange = range(start, start + 9)
    min = 99999999
    max = 0
    for product in listAllProduct:
        if (product.discount_price == 0 or product.discount_price == None):
            if min > product.price:
                min = product.price
            if max < product.price:
                max = product.price
        else:
            if min > product.discount_price:
                min = product.discount_price
            if max < product.discount_price:
                max = product.discount_price
    for i in inrange:
        if i < listAllProduct.count():
            listProduct.append(listAllProduct[i])
        else:
            break
    cartid = request.COOKIES.get('cartid')
    if cartid != None:
        cart = Cart.objects.get(pk=cartid)
    else:
        cart = Cart()
        cart.save()
    listCartItem = cart.cartitem_set.filter(is_bought = False)
    total = 0
    for item in listCartItem:
        if item.product.discount_price != 0:
            total += (item.quantity * item.product.discount_price)
        else:
            total += (item.quantity * item.product.price)
    context = {
        "listCate": listAllCate,
        "listType": listAllType,
        "listProduct": listProduct,
        "start": (start + 9),
        "min": min,
        "max": max,
        "sort":sort,
        "listCartItem": listCartItem,
        "cart": cart,
        "total": total,
        "status": "sorttype",
        "type":type,
        "user":user
    }
    return render(request, "homepage/shop.html", context)