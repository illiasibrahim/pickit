from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('sign-in/',views.sign_in,name='sign-in'),
    path('verify-sign/',views.verify_signin, name='verify-signin'),
    path('sign-up/',views.sign_up,name='sign-up'),
    path('verify-signup/',views.verify_signup,name='verify-signup'),
    path('verified-user/',views.verified_user,name='verified-user'),
    path('logout/',views.logout,name='logout'),
    path('product/<product_id>/',views.product_detail, name='product'),
    path('store/',views.store,name='store'),
    path('search/',views.search,name='search'),
    path('category/<category_id>/',views.category_view,name='category'),
    path('cart/',views.cart,name='cart'),
    path('add-cart/',views.add_cart,name='add-cart'),
    path('remove-cart/',views.remove_cart, name='remove-cart'),
    path('remove-cart-item/<int:product_id>/',views.remove_cart_item,name='remove-cart-item')
    
]