from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('sign-in/',views.sign_in,name='sign-in'),
    path('verify-sign/',views.verify_signin, name='verify-signin'),
    path('signin-password',views.signin_password,name='signin-password'),
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
    path('remove-cart-item/<int:product_id>/',views.remove_cart_item,name='remove-cart-item'),
    path('checkout/',views.checkout,name="checkout"),
    path('add-address/',views.add_address,name="add-address"),
    path('account/',views.account,name="account"),
    path('profile/',views.profile,name='profile'),
    path('change-dp/',views.change_dp,name='change-dp'),
    path('change-password/',views.change_password,name='change-password'),
    path('saved-address/',views.saved_address,name='saved-address'),
    path('delete-address/<address_id>/',views.delete_address,name='delete-address'),
    path('make-default/<address_id>/',views.make_default,name='make-default'),
    path('new-address/',views.new_address,name='new-address'),
    


    
]