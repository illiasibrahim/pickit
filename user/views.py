from django.contrib.auth import SESSION_KEY, backends
from django.core import paginator
from django.db.models.query import RawQuerySet
from django.http.response import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect, resolve_url
from vendor.models import Banner,Category,Poster,Product
from .models import Account,CartItem, Cart, DeliveryAddress,DefaultAddress, Profile
from .forms import AddressForm,ProfileForm
from django.contrib import messages,auth
import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from twilio.rest import Client
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import sessions


import json

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


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            username = email.split('@')[0]
            password = request.POST['password']
            print(password)
            
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

                otp = random.randint(1000,9999)
                request.session['otp'] = otp
                print(otp)
                # account_sid = 'ACebf98e0fff644ccb36708cc0984af114'
                # auth_token = 'bbb861541cffc9f84cdbf8f47612d672'
                # client = Client(account_sid, auth_token)
                # message = client.messages.create(
                #                                 body= f'Your OTP for registration is -{ otp }',
                #                                 from_='+17816615925',
                #                                 to=f'+91{phone}'
                #                             )

                return redirect('verify-signup')

        return render(request,'user/register.html')


def verify_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            otp = str(request.session['otp'])
            entered_otp = str(request.POST['otp'])
            if otp == entered_otp:
                phone = request.session['phone']
                email = request.session['email']
                first_name = request.session['first_name']
                last_name = request.session['last_name']
                username = request.session['username']
                password = request.session['password']
                print(password)

                del request.session['otp']
                del request.session['email']
                del request.session['first_name']
                del request.session['last_name']
                del request.session['username']

                user = Account.objects.create_user(phone=phone, email=email, first_name=first_name, last_name=last_name,username=username,password=password)
                user.save()
                return redirect('verified-user')
            else:
                messages.info(request,'The OTP you entered is wrong please try again',extra_tags='wrong otp')
        return render(request,'user/verify_otp.html')

# sign-in functions

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            phone = request.POST['phone']
            request.session['phone']=phone
            user = Account.objects.get(phone=phone)
            print(user)
            if user is not None:
                if user.has_access:
                    otp = random.randint(1000,9999)
                    # account_sid = 'ACebf98e0fff644ccb36708cc0984af114'
                    # auth_token = 'bbb861541cffc9f84cdbf8f47612d672'
                    # client = Client(account_sid, auth_token)
                    # message = client.messages.create(
                    #                                 body= f'Your OTP for registration is -{ otp }',
                    #                                 from_='+17816615925',
                    #                                 to=f'+91{phone}'
                    #                             )
                    print(otp)
                    request.session['otp'] = otp
                    return redirect('verify-signin')
                else:
                    messages.info(request,'This account is been blocked')
            else:
                messages.info(request,'This number is not registerd in pickit !')
        return render(request,'user/signin.html')


def verify_signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            otp = str(request.session['otp'])
            entered_otp = str(request.POST['otp'])
            if otp == entered_otp:
                phone = request.session['phone']
                user = auth.authenticate(phone=phone)
                auth.login(request,user)
                return redirect('home')
            else:
                messages.info(request,'The OTP you entered is wrong please try again',extra_tags='wrong otp')
        return render(request,'user/verify_otp.html')


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
                    auth.login(request,user)
                    return redirect('home')
                else:
                    messages.info(request,'This account is been blocked')
            else:
                messages.info(request,'Invalid login credentials')
        return redirect('sign-in')

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
                is_user_cart_exists = CartItem.objects.filter(user=user).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart = cart)
                    if is_user_cart_exists:
                        user_cart = CartItem.objects.filter(user=user)
                        for item in cart_item:
                            for user_item in user_cart:
                                if item.product == user_item.product:
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
            auth.login(request, user)
            return redirect('/')
        return redirect('sign-in')


@login_required(login_url='home')
def logout(request):
    auth.logout(request)
    return redirect('/')


def store(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    product_count = products.count()
    paginator = Paginator(products,8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {'products':paged_products, 'product_count':product_count,'categories':categories}
    return render(request,'user/store.html',context)


def product_detail(request,product_id):
    product = Product.objects.get(id= product_id)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
    cart_item = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product)

    context = {
        'product' : product,
        'in_cart': in_cart,
        'cart_item':cart_item,
    }
    return render(request, 'user/product_detail.html',context)


def search(request):
    categories = Category.objects.all()
    search_key = request.GET['search_key']
    if search_key == "":
        paged_products = None
        product_count = 0
    else:
        results = Product.objects.filter(Q(product_name__icontains=search_key) | Q(brand__brand_name__icontains=search_key) |Q(category__category_name__icontains=search_key))
        product_count = results.count() 
        paginator = Paginator(results,4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    context = {'products':paged_products ,'product_count':product_count, 'categories':categories,'search_key':search_key}
    return render(request, 'user/search_result.html', context)


def category_view(request, category_id):
    categories = Category.objects.all()
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category_id = category_id)  
    product_count = products.count() 
    paginator = Paginator(products,4)
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
        for cart_item in cart_items:
            total += (cart_item.product.discount_price * cart_item.quantity)
            quantity += cart_item.quantity
    except :
        pass
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
            cart_item = CartItem.objects.get(product=product,user = request.user)
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
    if request.user.is_authenticated:
        cart_items = CartItem.objects.all().filter(user=request.user)
    else:
        cart_items = CartItem.objects.all().filter(cart=cart)
    for cart_ite in cart_items: #inorder to avoid conflict with same name cartite
        cart_count += int(cart_ite.quantity)
        print('working')
    ind_count = cart_item.quantity
    return JsonResponse({'data':cart_count,'ind_count':ind_count})
    

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
    for cart_ite in cart_items: #inorder to avoid conflict with same name cartitem and cartite
        cart_count += int(cart_ite.quantity)
    ind_count = cart_item.quantity
    return JsonResponse({'data':cart_count,'ind_count':ind_count,'rem':rem})

def remove_cart_item(request,product_id): # to remove the entire quantity of a purticular cart item
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='sign-in')
def checkout(request):
    try:
        total = 0
        quantity =0
        discount = 0
        total_mrp =0
        cart_items = None
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total_mrp += (cart_item.product.mrp * cart_item.quantity)
            total += (cart_item.product.discount_price * cart_item.quantity)
            discount += (cart_item.product.discount * cart_item.quantity)
            quantity += cart_item.quantity
    except:
        pass
    delivery_addresses = DeliveryAddress.objects.filter(user=request.user)
    is_default = DefaultAddress.objects.filter(user=request.user).exists()
    address_form = AddressForm()
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'discount':discount,
        'total_mrp':total_mrp,
        'delivery_addresses':delivery_addresses,
        'address_form':address_form,
    }
    if is_default:
        default_address = DefaultAddress.objects.get(user=request.user)
        context['default_address']=default_address
    return render(request,'user/place_order.html',context)



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

@login_required(login_url='sign-in')       
def account(request):
    context = {

    }
    return render(request,'user/dashboard.html',context)

def profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        user_id = request.user.id
        user = Account.objects.get(id=user_id)

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
    else:
        user = request.user
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            profile = Profile.objects.create(user=request.user)
            profile.dispaly_picture = None
            profile.save()
    profile_form = ProfileForm()
    context = {
        'user':user,
        'profile':profile,
        'profile_form':profile_form
        }
    return render(request,'user/profile.html',context)

def change_dp(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            display = profile_form.cleaned_data.get('display_picture')
            print(display)
            try:
                profile = Profile.objects.get(user=request.user)
            except:
                profile = Profile.objects.create(user=request.user)
            profile.display_picture = display
            profile.save()
            return redirect('profile')


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

def delete_address(request,address_id):
    DeliveryAddress.objects.filter(user=request.user,id=address_id).delete()
    return redirect('saved-address')

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
