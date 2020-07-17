from django.urls import path

from .views import (
    item_detail, CheckoutView, remove_from_cart,
    remove_single_item_from_cart, required_product, product_list, admin_order_pdf, UserProfile, Tracker,
    user_order_pdf, item_search, user_profile, order_history,
    add_to_cart, order_summary, Ins, testview
    # OrderSummaryView
)

app_name = 'core'
urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    # path('', ItemDetailView.as_view(), name='home'),
    path('', product_list, name='product_list'),
    path('required-product/', required_product, name='required_product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    #     path('product/<slug>', ItemDetailView.as_view(), name='product_detail'),
    path('product/<slug>', item_detail, name='product_detail'),

    path('product/<slug:category_slug>/', product_list,
         name='product_list_by_category'),  # Added Later
    # path('checkout/', checkout, name='checkout'),
    path('add-to-cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove_from_cart'),
    #     path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
    path('admin/order/<int:order_id>/pdf/',
         admin_order_pdf, name='admin_order_pdf'),
    path('profile/<int:pk>', UserProfile.as_view(), name='user_profile'),
    path('tracker/', Tracker, name='tracker'),
    path('invoice/<order_id>', user_order_pdf, name='user_invoice'),
    path('search/', item_search, name='search'),
    path('profile/', user_profile, name='profile'),
    path('order-history/', order_history, name='order_history'),
    path('order-summary/', order_summary, name='order_summary'),
    path('Instructions/', Ins, name='Instructions'),
    path('testview/', testview, name='testview')
]
