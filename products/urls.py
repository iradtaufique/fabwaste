from django.urls import path
from .views import addProduct, houseHoldProducts, updateHouseHoldProducts, productStatus, \
    productUpdate, device_details, add_buying_price, manufacture_device_details, add_selling_price, denied_product, \
    list_ready_for_sold_products, list_waste_products, list_published_products, list_requested_products, \
    published_details, ready_for_sold_details

urlpatterns = [
    path('add-product', addProduct, name='add_product'),
    path('view-product', houseHoldProducts, name='view_product'),
    path('update-product/<int:id>', updateHouseHoldProducts, name='household_update_product'),
    path('pending-product', productStatus, name='pending'),
    path('rejected-product', productStatus, name='rejected'),
    path('collected-product', productStatus, name='collected'),
    path('update/<int:id>/', productUpdate, name='product_update'),
    path('device-details/<int:pk>/', device_details, name='device_details'),
    path('deny-product/<int:pk>/', denied_product, name='deny_product'),
    path('manufacture-device-details/<int:pk>/', manufacture_device_details, name='manufacture_device_details'),
    path('add-buying-price/<int:pk>/', add_buying_price, name='add_buying_price'),
    path('add-selling-price/<int:pk>/', add_selling_price, name='add_selling_price'),

    path('ready-for-sold/', list_ready_for_sold_products, name='ready_for_sold'),
    path('waste-products/', list_waste_products, name='waste_product'),
    path('published-products/', list_published_products, name='published_product'),
    path('requested-products/', list_requested_products, name='requested_product'),
    path('published-details/<int:pk>/', published_details, name='published_details'),
    path('ready-for-sold-details/<int:pk>/', ready_for_sold_details, name='ready_for_sold_details'),

]
