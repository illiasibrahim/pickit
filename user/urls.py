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
    path('submit-review/<product_id>',views.submit_review,name='submit-review'),
    path('store/',views.store,name='store'),
    path('search/',views.search,name='search'),
    path('category/<category_id>/',views.category_view,name='category'),
    path('cart/',views.cart,name='cart'),
    path('add-cart/',views.add_cart,name='add-cart'),
    path('remove-cart/',views.remove_cart, name='remove-cart'),
    path('remove-cart-item/<int:product_id>/',views.remove_cart_item,name='remove-cart-item'),
    path('checkout/',views.checkout,name="checkout"),
    path('apply-coupon/',views.apply_coupon,name='apply-coupon'),
    path('place-order/',views.place_order,name="place-order"),
    path('paypal/',views.paypal,name='paypal'),
    path('razor/',views.razor,name='razor'),
    path('order-complete/',views.order_complete,name='order-complete'),
    path('cancel-order/<order_id>',views.cancel_order,name='cancel-order'),
    path('add-address/',views.add_address,name="add-address"),
    path('account/',views.account,name="account"),
    path('profile/',views.profile,name='profile'),
    path('change-dp/',views.change_dp,name='change-dp'),
    path('change-password/',views.change_password,name='change-password'),
    path('saved-address/',views.saved_address,name='saved-address'),
    path('delete-address/<address_id>/',views.delete_address,name='delete-address'),
    path('make-default/<address_id>/',views.make_default,name='make-default'),
    path('new-address/',views.new_address,name='new-address'),
    path('edit-address/',views.edit_address,name='edit-address'),    
    path('order-failed/',views.order_failed,name='order-failed'),


    
]