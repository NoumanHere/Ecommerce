from django.urls import path

from .views import (
    HomeView, ItemDetailView, products, checkout, add_to_cart, remove_from_cart, OrderSummaryView,
    remove_single_item_from_cart, required_product,product_list
)

app_name = 'core'
urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    # path('', ItemDetailView.as_view(), name='home'),
    path('', product_list, name='product_list'),
    path('required-product/', required_product, name='required_product'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>', ItemDetailView.as_view(), name='product'),
#     path('<slug:category_slug>/',product_list, 
#          name='product_list_by_category'),
    path('add-to-cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove_from_cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
]
