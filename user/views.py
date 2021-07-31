from typing import cast
from django.contrib.auth import SESSION_KEY, backends, login
from django.core import paginator
from django.db.models.query import RawQuerySet
from django.http.response import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect, resolve_url
from vendor.models import Banner,Category,Poster,Product
from .models import Account,CartItem, Cart, DeliveryAddress,DefaultAddress, Order,Payment,OrderProduct,Coupon, ReviewRating
from .forms import AddressForm,ProfileForm, ReviewRatingForm
from django.contrib import messages,auth
import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from twilio.rest import Client
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import sessions
import datetime
import json
from math import ceil,floor, log
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import razorpay
from twilio.rest import Client
from google_currency import convert
from decouple import config
from django.views.decorators.cache import never_cache
import hashlib

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart   


def home(request):
    banners = Banner.objects.filter(status = True)
    categories = Category.objects.all()
    posters = Poster.objects.filter(status = True)
    products = Product.objects.all().order_by('-offer')[0:12]
    context = {
        'banners' : banners,
        'categories' : categories,
        'posters' : posters,
        'products' : products,
    }
    return render(request,'user/index.html',context)

@never_cache
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            username = email.split('@')[0]+ str(random.randint(100,999))
            password = request.POST['password']
            
            if Account.objects.filter(email = email):
                messages.info(request,'This email address is already been used', extra_tags='email')
            elif Account.objects.filter(phone=phone):
                messages.info(request, 'This phone number is already been used',extra_tags='phone')
            else:
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['email'] = email
                request.session['phone'] = phone
                request.session['username'] = username
                request.session['password'] = password
                try:
                    account_sid = config('account_sid', cast=str)
                    auth_token = config('auth_token', cast=str)
                    client = Client(account_sid, auth_token)

                    verification = client.verify \
                        .services(config('services', cast=str)) \
                        .verifications \
                        .create(to=f'+91{phone}', channel='sms')


                    return redirect('verify-signup')
                except:
                    messages.info(request,'Some error occured with your mobile number',extra_tags='twilio')
                    return render(request,'user/register.html')

        return render(request,'user/register.html')

@never_cache
def verify_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            phone = request.session['phone']
            entered_otp = str(request.POST['otp'])

            account_sid = config('account_sid', cast=str)
            auth_token = config('auth_token', cast=str)
            client = Client(account_sid, auth_token)

            verification_check = client.verify \
                           .services(config('services', cast=str)) \
                           .verification_checks \
                           .create(to=f'+91{phone}', code=entered_otp)

            if verification_check.status == 'approved':
                
                email = request.session['email']
                first_name = request.session['first_name']
                last_name = request.session['last_name']
                username = request.session['username']
                password = request.session['password']

                del request.session['email']
                del request.session['first_name']
                del request.session['last_name']
                del request.session['username']

                user = Account.objects.create_user(phone=phone, email=email, first_name=first_name, last_name=last_name,username=username,password=password)
                user.save()
                return redirect('verified-user')
            else:
                messages.info(request,'The OTP you entered is wrong please try again',extra_tags='wrong otp')
        phone = request.session['phone']
        context = {'phone':phone,}
        return render(request,'user/verify_otp.html',context)

# sign-in functions

@never_cache
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            phone = request.POST['phone']
            request.session['phone']=phone
            try:
                user = Account.objects.get(phone=phone)
            except:
                user = None
            if user is not None:
                if user.has_access:
                    try:
                        account_sid = config('account_sid', cast=str)
                        auth_token = config('auth_token', cast=str)
                        client = Client(account_sid, auth_token)

                        verification = client.verify \
                        .services(config('services', cast=str)) \
                        .verifications \
                        .create(to=f'+91{phone}', channel='sms')

                        return redirect('verify-signin')
                    except:
                        messages.info(request,'There is something error with your entered mobile numbrer',extra_tags='twilio_sign_in')
                else:
                    messages.info(request,'This account is been blocked',extra_tags='blocked')
            else:
                messages.info(request,'This number is not registerd in pickit !',extra_tags='not-registered')
        return render(request,'user/signin.html')


@never_cache
def verify_signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            entered_otp = str(request.POST['otp'])
            phone = request.session['phone']

            account_sid = config('account_sid', cast=str)
            auth_token = config('auth_token', cast=str)
            client = Client(account_sid, auth_token)

            verification_check = client.verify \
                           .services(config('services', cast=str)) \
                           .verification_checks \
                           .create(to=f'+91{phone}', code=entered_otp)

            if verification_check.status == 'approved':
                user = auth.authenticate(phone=phone)
                try:
                    cart = Cart.objects.get(cart_id = _cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    is_user_cart_exists = CartItem.objects.filter(user=user).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart = cart)
                        if is_user_cart_exists:
                            for item in cart_item:
                                is_item_exists = CartItem.objects.filter(user=user,product=item.product).exists()
                                if is_item_exists:
                                    user_item = CartItem.objects.get(user=user,product=item.product)
                                    user_item.quantity += item.quantity
                                    user_item.save()
                                else:
                                    item.user = user
                                    item.save()
                        else:
                            for item in cart_item:
                                item.user = user 
                                item.save()
                except:
                    pass
                auth.login(request,user)
                return redirect('home')
            else:
                messages.info(request,'The OTP you entered is wrong please try again',extra_tags='wrong otp')
        phone = request.session['phone']
        context = {'phone':phone}
        return render(request,'user/verify_otp.html',context)


@never_cache
def signin_password(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            phone = request.POST['phone']
            password = request.POST['password']
            user = auth.authenticate(phone = phone, password = password)
            if user is not None:
                if user.has_access:
                    try:
                        cart = Cart.objects.get(cart_id = _cart_id(request))
                        is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                        is_user_cart_exists = CartItem.objects.filter(user=user).exists()
                        if is_cart_item_exists:
                            cart_item = CartItem.objects.filter(cart = cart)
                            if is_user_cart_exists:
                                for item in cart_item:
                                    is_item_exists = CartItem.objects.filter(user=user,product=item.product).exists()
                                    if is_item_exists:
                                        user_item = CartItem.objects.get(user=user,product=item.product)
                                        user_item.quantity += item.quantity
                                        user_item.save()
                                    else:
                                        item.user = user
                                        item.save()
                            else:
                                for item in cart_item:
                                    item.user = user 
                                    item.save()
                    except:
                        pass
                    auth.login(request,user)
                    return redirect('home')
                else:
                    messages.info(request,'This account is been blocked','blocked')
            else:
                messages.info(request,'Invalid login credentials','invalid')
        return redirect('sign-in')

@never_cache
# this is to login a verified user either signed up or signed in
def verified_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.session.has_key('phone'):
            phone = request.session['phone']
            password = request.session['password']
            user = auth.authenticate(phone=phone,password=password)
            del request.session['phone']
            del request.session['password']
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart = cart)
                    for item in cart_item:
                        item.user = user 
                        item.save()
            except:
                pass
            auth.login(request, user)
            return redirect('/')
        return redirect('sign-in')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')
    else:
        return redirect('home')



def store(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    product_count = products.count()
    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {'products':paged_products, 'product_count':product_count,'categories':categories}
    return render(request,'user/store.html',context)


def product_detail(request,product_id):
    product = Product.objects.get(id= product_id)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
    cart_item = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product)
    try:
        purchased = OrderProduct.objects.filter(user=request.user,product=product).exists()
    except:
        purchased = False
    reviews = ReviewRating.objects.filter(product=product,status= True)
    average_rating = 0
    for review in reviews:
        average_rating += review.rating
    rating_count = reviews.count()
    if reviews:
        average_rating = average_rating/rating_count
    context = {
        'product' : product,
        'in_cart': in_cart,
        'cart_item':cart_item,
        'purchased':purchased,
        'reviews':reviews,
        'average_rating':average_rating,
        'rating_count':rating_count,
    }
    return render(request, 'user/product_detail.html',context)


@login_required(login_url='sign-in')
def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user=request.user,product__id=product_id)
            form = ReviewRatingForm(request.POST,instance=review)
            form.save()
            if form.is_valid():
                return redirect(url)
        except:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                return redirect(url)


def search(request):
    categories = Category.objects.all()
    search_key = request.GET['search_key']
    if search_key == "":
        paged_products = None
        product_count = 0
    else:
        results = Product.objects.filter(Q(product_name__icontains=search_key) | Q(brand__brand_name__icontains=search_key) |Q(category__category_name__icontains=search_key))
        product_count = results.count() 
        paginator = Paginator(results,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    context = {'products':paged_products ,'product_count':product_count, 'categories':categories,'search_key':search_key}
    return render(request, 'user/search_result.html', context)


def category_view(request, category_id):
    categories = Category.objects.all()
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category_id = category_id)  
    product_count = products.count() 
    paginator = Paginator(products,12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {'products':paged_products, 'category':category,'product_count':product_count,'categories':categories}
    return render(request,'user/category.html',context)

 
def cart(request):
    try:
        total = 0
        quantity =0
        cart_items = None
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        
    except :
        pass
    if cart_items:
        for cart_item in cart_items:
            total += (int(cart_item.product.selling_price()) * int(cart_item.quantity))
            quantity += cart_item.quantity
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    return render(request,'user/cart.html',context)



def add_cart(request):
    cart_items = None
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
            except:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
            cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 
        cart_item.save()
    except :
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user
            )
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity =1,
                cart = cart,
            )
        cart_item.save()
    cart_count = 0
    cart_value = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.all().filter(user=request.user)
    else:
        cart_items = CartItem.objects.all().filter(cart=cart)
    for cart_ite in cart_items: #inorder to avoid conflict with same name cartite
        cart_count += 1
        cart_value += int(cart_ite.quantity)* int(cart_ite.product.selling_price())
    ind_count = cart_item.quantity
    ind_price = int(cart_item.quantity) * int(cart_item.product.selling_price())
    return JsonResponse({'data':cart_count,'ind_count':ind_count,'ind_price':ind_price,'cart_value':cart_value})
    

def remove_cart(request): # to remove single quantity of a purticular cart item
    rem = False
    product_id = request.GET['product_id']
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user)
        cart_items = CartItem.objects.all().filter(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_items = CartItem.objects.all().filter(cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        rem = True # to remove the item from cart without reloading
    cart_count = 0
    cart_value = 0
    for cart_ite in cart_items: #inorder to avoid conflict with same name cartitem and cartite
        cart_count += 1
        cart_value += int(cart_ite.quantity)* int(cart_ite.product.selling_price())
    ind_count = cart_item.quantity
    ind_price = int(cart_item.quantity) * int(cart_item.product.selling_price())
    return JsonResponse({'data':cart_count,'ind_count':ind_count,'rem':rem,'ind_price':ind_price,'cart_value':cart_value})


def remove_cart_item(request,product_id): # to remove the entire quantity of a purticular cart item
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


# checkout

@never_cache
@login_required(login_url='sign-in')
def checkout(request):
    total = 0
    discount = 0
    total_mrp =0
    cart_items = None
    
    cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    if not cart_items:
        return redirect('home')
    for cart_item in cart_items:
        total_mrp += (cart_item.product.mrp * cart_item.quantity)
        total += (cart_item.product.selling_price() * cart_item.quantity)
        discount += (cart_item.product.discount_amount() * cart_item.quantity)
    if request.method == 'POST':
        order = Order()
        selected = request.POST['delivery-address']
        if selected == "add_new":
            form = AddressForm(request.POST)
            if form.is_valid():
                try:
                    save_address = request.POST['save_address']
                except:
                    save_address = None
                if save_address  == "save":
                    address = DeliveryAddress()
                    address.first_name = form.cleaned_data['first_name']
                    address.last_name = form.cleaned_data['last_name']
                    address.phone = form.cleaned_data['phone']
                    address.state = form.cleaned_data['state']
                    address.country = form.cleaned_data['country']
                    address.street = form.cleaned_data['street']
                    address.city = form.cleaned_data['city']
                    address.pin = form.cleaned_data['pin']
                    address.building = form.cleaned_data['building']
                    address.landmark = form.cleaned_data['landmark']
                    address.user = request.user
                    address.save()
                    
                order.first_name = form.cleaned_data['first_name']
                order.last_name = form.cleaned_data['last_name']
                order.phone = form.cleaned_data['phone']
                order.state = form.cleaned_data['state']
                order.country = form.cleaned_data['country']
                order.street = form.cleaned_data['street']
                order.city = form.cleaned_data['city']
                order.pin = form.cleaned_data['pin']
                order.building = form.cleaned_data['building']
                order.landmark = form.cleaned_data['landmark']
                
        
        else:
            delivery_address = DeliveryAddress.objects.get(id=selected)
            order.first_name = delivery_address.first_name
            order.last_name = delivery_address.last_name
            order.phone = delivery_address.phone
            order.state = delivery_address.state
            order.country = delivery_address.country
            order.street = delivery_address.street
            order.city = delivery_address.city
            order.pin = delivery_address.pin
            order.building = delivery_address.building
            order.landmark = delivery_address.landmark
        order.user = request.user
        order.order_total = total_mrp
        order.order_discount = discount
        order.total = total
        order.ip = request.META.get('REMOTE_ADDR')
        order.save()
        # generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(order.id)
        order.order_number = order_number
        order.save()
        request.session['order_number'] = order_number
        return redirect('place-order')

    delivery_addresses = DeliveryAddress.objects.filter(user=request.user)
    is_default = DefaultAddress.objects.filter(user=request.user).exists()
    address_form = AddressForm()
    context = {
        'total':total,
        'cart_items':cart_items,
        'discount':discount,
        'total_mrp':total_mrp,
        'delivery_addresses':delivery_addresses,
        'address_form':address_form,
    }
    if is_default:
        default_address = DefaultAddress.objects.get(user=request.user)
        context['default_address']=default_address
    return render(request,'user/checkout.html',context)


# place order
@never_cache
@login_required(login_url='sign-in')
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    discount = 0
    total_mrp =0
    if not cart_items:
        return redirect('home')
    for cart_item in cart_items:
        total_mrp += (cart_item.product.mrp * cart_item.quantity)
        discount += (cart_item.product.discount_amount() * cart_item.quantity)
    order_number = request.session['order_number']
    order = Order.objects.get(user= request.user,is_ordered=False,order_number=order_number)
    coupon_discount = '0'
    if order.coupon is not None:
        coupon_discount = int(order.order_total)-int(order.order_discount)-int(order.total)
    total = int(order.total) * 100
    # to convert currency from usd to inr for paypal transaction
    converted = convert('inr', 'usd',order.total)
    json_object = json.loads(converted)
    converted_amount = json_object['amount']
    auth1= config('razorpayauth1',cast=str)
    auth2= config('razorpayauth2',cast=str)
    client = razorpay.Client(auth=(auth1, auth2))
    order_amount = int(order.total)*100
    razorpay_order = client.order.create({'amount':order_amount,'currency':'INR'})
    request.session['order_id']=razorpay_order['id']
    context = {
        'order_id':razorpay_order['id'],
        'order':order,
        'total':total,
        'cart_items':cart_items,
        'discount':discount,
        'total_mrp':total_mrp,
        'coupon_discount':coupon_discount,
        'converted_amount':converted_amount,
    }
    return render(request,'user/place_order.html',context)


@login_required(login_url='sign-in')
def apply_coupon(request):
    order_id = request.GET['order_id']
    coupon_code = request.GET['coupon_code']
    try:
        coupon = Coupon.objects.get(code=coupon_code)
    except:
        coupon = None
    if coupon is not None:
        if coupon.status:
            try:
                previous_order = Order.objects.get(user=request.user,coupon=coupon,is_ordered=True)
            except:
                previous_order = None
            if previous_order is None:
                order = Order.objects.get(id=order_id)
                order.coupon = coupon
                total = ceil((int(order.order_total)-int(order.order_discount))*(1-(int(coupon.discount)/100)))
                order.total = total
                order.save()
                coupon_discount = floor(((int(order.order_total)-int(order.order_discount)))*(int(coupon.discount)/100))
                res = {'order_total':order.total,'coupon_code':coupon.code,'coupon_discount':coupon_discount}
            else:
                res = {'applied':'applied'}
        else:
            res ={'expired':'expired'}
    else:
        res = {'none':'none'}
    return JsonResponse(res)




# payments
login_required(login_url='sign-in')
def paypal(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False,order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transactionID'],
        payment_method = body['payment_method'],
        amount_paid = order.total,
        status = body['status']
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # move cart item to order product table
    cart_item = CartItem.objects.filter(user=request.user)

    for item in cart_item:
        order_product = OrderProduct()
        order_product.order = order
        order_product.payment = payment
        order_product.user = request.user
        order_product.product = item.product
        order_product.quantity = item.quantity
        order_product.product_price = item.product.selling_price()
        order_product.ordered = True
        order_product.save()

    # clear cart
    CartItem.objects.filter(user=request.user).delete()
    data = {
        'order_number' : order.order_number,
        'transID' : payment.payment_id
    }

    return JsonResponse(data)



def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


login_required(login_url='sign-in')
def razor(request):
    response = request.POST
    # auth1= config('razorpayauth1',cast=str)
    # auth2= config('razorpayauth2',cast=str)
    # order_number = request.session['order_number']
    # order = Order.objects.get(user=request.user, is_ordered=False,order_number=order_number)
    # order_id = request.session['order_id']
    # razorpay_payment_id = response['razorpay_payment_id']
    # secret = auth2
    # string = order_id + "|" + razorpay_payment_id
    # print(secret)
    # generated_signature = encrypt_string(string)
    # print(generated_signature)
    # print(response)
    # params_dict = {
    # 'razorpay_order_id': response['razorpay_order_id'],
    # 'razorpay_payment_id': response['razorpay_payment_id'],
    # 'razorpay_signature': response['razorpay_signature']
    # }
    # client = razorpay.Client(auth=(auth1, auth2))

    try:
        order_number = request.session['order_number']
        order = Order.objects.get(user=request.user, is_ordered=False,order_number=order_number)
        payment = Payment(
            user = request.user,
            payment_id = response['razorpay_payment_id'],
            payment_method = 'razorpay',
            amount_paid = order.total,
            status = 'COMPLETED'
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        # move cart item to order product table
        cart_item = CartItem.objects.filter(user=request.user)

        for item in cart_item:
            order_product = OrderProduct()
            order_product.order = order
            order_product.payment = payment
            order_product.user = request.user
            order_product.product = item.product
            order_product.quantity = item.quantity
            order_product.product_price = item.product.selling_price()
            order_product.ordered = True
            order_product.save()

        # clear cart
        CartItem.objects.filter(user=request.user).delete()
        return redirect('order-complete')
    except:
        return redirect('order-failed')
    

@never_cache
@login_required(login_url='sign-in')
def order_complete(request):
    total_mrp = 0
    total = 0
    discount = 0
    try:
        order_number = request.session['order_number']
    except:
        return redirect('home')
    order = Order.objects.get(user=request.user, is_ordered=True,order_number=order_number)
    products = OrderProduct.objects.filter(order=order)
    for product in products:
        total_mrp += (product.product.mrp * product.quantity)
        total += (product.product.selling_price() * product.quantity)
        discount += (product.product.discount_amount() * product.quantity)
    coupon_discount = 0
    if order.coupon is not None:
        coupon_discount = floor(int(order.coupon.discount)/100 * int(total))
        discount = int(discount) + int(coupon_discount)
    context = {
        'order':order,
        'products':products,
        'total_mrp':total_mrp,
        'total':total,
        'discount':discount,
        'coupon_discount':coupon_discount,
    }
    del request.session['order_number']
    return render(request,'user/order_complete.html',context)

@never_cache
@login_required(login_url='sign-in')
def order_failed(request):
    try:
        order_number = request.session['order_number']
    except:
        return redirect('home')
    del request.session['order_number']
    return render(request,'user/order_failed.html')


# add addresss
@login_required(login_url='sign-in')
def add_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        is_default = DefaultAddress.objects.filter(user=request.user).exists()
        if address_form.is_valid:
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            if is_default:
                default_address = DefaultAddress.objects.get(user=request.user)
                default_address.default_address = new_address
                default_address.save()
            else:
                default_address = DefaultAddress.objects.create(user=request.user, default_address=new_address)
                default_address.save()
            return redirect('checkout')
    return redirect('checkout')

@never_cache
@login_required(login_url='sign-in')       
def account(request):
    orders = Order.objects.all().filter(user=request.user,is_ordered=True).order_by('-created_at')
    order_products = OrderProduct.objects.all().filter(user=request.user)
    context = {
        'orders':orders,
        'order_products':order_products
    }
    return render(request,'user/dashboard.html',context)


@login_required(login_url='sign-in') 
def cancel_order(request,order_id):
    try:
        order = Order.objects.get(id=order_id)
    except:
        return redirect('account')
    order.status = "Cancelled"
    order.save()
    return redirect('account')

@never_cache
@login_required(login_url='sign-in') 
def profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        user_id = request.user.id
        try:
            user = Account.objects.get(id=user_id)
        except:
            return redirect('sign-in')

        if username != user.username:
            if Account.objects.filter(username=username).exists():
                messages.info(request,'Sorry, this username is already been taken',extra_tags='username')
            else:
                user.username = username
        if email != user.email:
            if Account.objects.filter(email = email).exists():
                messages.info(request,'This email address is already been registered with another account',extra_tags='email')
            else:
                user.email = email
        if phone != user.phone:
            if Account.objects.filter(phone=phone):
                messages.info(request,'This mobile number is already been registered in pickit')
            else:
                user.phone = phone
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('profile')
    user = request.user
    profile_form = ProfileForm()
    context = {
        'user':user,
        'profile_form':profile_form
        }
    return render(request,'user/profile.html',context)

@login_required(login_url='sign-in')
def change_dp(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            display = profile_form.cleaned_data.get('display_picture')
            profile = request.user
            profile.display_picture = display
            profile.save()
            return redirect('profile')

@never_cache
@login_required(login_url='sign-in')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            messages.info(request,'Your password has been updated successfully',extra_tags='success')
        else:
            messages.info(request,'You entered a wrong password',extra_tags='fail')
    return render(request,'user/change_password.html')


@never_cache
@login_required(login_url='sign-in')
def saved_address(request):
    addresses = DeliveryAddress.objects.all().filter(user=request.user)
    is_default = default = DefaultAddress.objects.filter(user=request.user).exists()
    if is_default:
        default = DefaultAddress.objects.get(user = request.user)
    address_form = AddressForm()
    context = {
        'addresses' : addresses,
        'default': default,
        'is_default':is_default,
        'address_form':address_form,
    }
    return render(request,'user/addresses.html',context)


@login_required(login_url='sign-in')
def new_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid:
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('saved-address')
    return redirect('saved-address')


@login_required(login_url='sign-in')
def edit_address(request):
    if request.method == 'POST':
        id = request.POST['id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        street = request.POST['street']
        building = request.POST['house']
        city = request.POST['city']
        landmark = request.POST['landmark']
        state = request.POST['state']
        country = request.POST['country']
        pin = request.POST['pin']
        address = DeliveryAddress.objects.get(id=id)
        address.first_name = first_name
        address.last_name = last_name
        address.phone = phone
        address.country = country
        address.state = state
        address.street = street
        address.city = city
        address.pin = pin
        address.building = building
        address.landmark = landmark
        address.save()
        return redirect('saved-address')
    address_id = request.GET['address_id']
    address = DeliveryAddress.objects.get(id=address_id)
    first_name = address.first_name
    last_name = address.last_name
    phone = address.phone
    country = address.country
    state = address.state
    street = address.street
    city = address.city
    pin = address.pin
    building = address.building
    landmark = address.landmark
    

    data = {
        'first_name':first_name,
        'last_name':last_name,
        'phone':phone,
        'country':country,
        'state':state,
        'street':street,
        'city':city,
        'pin':pin,
        'building':building,
        'landmark':landmark,
        'id': address_id,
    }
    return JsonResponse(data)

@login_required(login_url='sign-in')
def delete_address(request,address_id):
    DeliveryAddress.objects.filter(user=request.user,id=address_id).delete()
    return redirect('saved-address')

@login_required(login_url='sign-in')
def make_default(request,address_id):
    address = DeliveryAddress.objects.get(id=address_id)
    is_default = default = DefaultAddress.objects.filter(user=request.user).exists()
    if is_default:
        default = DefaultAddress.objects.get(user = request.user)
        default.default_address = address
    else:
        default = DefaultAddress.objects.create(user=request.user, default_address=address)
    default.save()
    return redirect('saved-address')


