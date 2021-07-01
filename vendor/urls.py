from collections import namedtuple
from django.urls import path
from . import views

urlpatterns = [
    path('',views.sign_in,name='admin-sign-in'),
    path('admin-logout/',views.logout,name='admin-logout'),
    path('dashboard/',views.dashboard,name='dashboard'),

    path('category/',views.category_view,name='category'),
    path('add-category/',views.add_category,name='add-category'),
    path('delete-category/<category_id>/',views.delete_category,name='delete-category'),
    path('edit-category/<category_id>/',views.edit_category,name='edit-category'),

    path('brand/',views.brand_view, name='brand'),
    path('add-brand',views.add_brand, name='add-brand'),
    path('delete-brand/<brand_id>',views.delete_brand, name='delete-brand'),
    path('edit-brand/<brand_id>',views.edit_brand, name='edit-brand'),

    path('product/',views.product_view, name='product'),
    path('add-product/',views.add_product, name='add-product'),
    path('delete-product/<product_id>',views.delete_product,name='delete-product'),
    path('edit-product/<product_id>',views.edit_product,name='edit-product'),

    path('banner/',views.banner_view,name='banner'),
    path('add-banner/',views.add_banner, name='add-banner'),
    path('delete-banner/<banner_id>',views.delete_banner, name='delete-banner'),
    path('edit-banner/<banner_id>', views.edit_banner, name='edit-banner'),

    path('poster/',views.poster_view, name='poster'),
    path('add-poster/', views.add_poster, name='add-poster'),
    path('delete-poster/<poster_id>', views.delete_poster, name='delete-poster'),
    path('edit-poster/<poster_id>', views.edit_poster, name='edit-poster'),

    path('user/',views.user_view, name='user'),
    path('delete-user/<user_id>/',views.delete_user,name='delete-user'),
    path('block-user/<user_id>',views.block_user, name='block-user'),
    path('unblock-user/<user_id>',views.unblock_user, name='unblock-user'),

    path('order/',views.order_view,name='order'),
    path('approve/',views.approve,name='approve'),
    path('dispatch/',views.dispatch,name='dispatch'),
    path('deliver/',views.deliver,name='deliver'),
    path('reject/',views.reject,name='reject'),

    path('coupon/',views.coupon_view,name='coupon'),
    path('add-coupon/',views.add_coupon,name='add-coupon'),
    path('delete-coupon/<coupon_id>/',views.delete_coupon,name='delete-coupon'),
    path('edit-coupon/<coupon_id>/',views.edit_coupon,name='edit-coupon'),
    path('update-category-offer/',views.update_cat_offer,name='update-category-offer'),
    path('delete-category-offer/',views.delete_cat_offer,name='delete-category-offer'),


   
]