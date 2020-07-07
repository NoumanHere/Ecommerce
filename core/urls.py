from django.urls import path

from .views import (
    HomeView, ItemDetailView, products, CheckoutView, add_to_cart, remove_from_cart, OrderSummaryView,
    remove_single_item_from_cart, required_product, product_list, admin_order_pdf, UserProfile,Tracker,
    user_order_pdf
)

app_name = 'core'
urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    # path('', ItemDetailView.as_view(), name='home'),
    path('', product_list, name='product_list'),
    path('required-product/', required_product, name='required_product'),
<<<<<<< HEAD
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('', product_list, name='product_list'),
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
    path('product/<slug:category_slug>/', product_list,name='product_list_by_category'),#Added Later
=======
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
#     path('<slug:category_slug>/',product_list, 
#          name='product_list_by_category'),
>>>>>>> 8e79960e736869fa88c3d9b3e3e2e5768ff075bd
    path('add-to-cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove_from_cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
    path('admin/order/<int:order_id>/pdf/',
         admin_order_pdf, name='admin_order_pdf'),
    path('profile/<int:pk>', UserProfile.as_view(), name='user_profile'),
    path('tracker/',Tracker,name = 'tracker'),
  path('invoice/',user_order_pdf,name = 'user_invoice')
]