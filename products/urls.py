from django.urls import path
from .views import addProduct, houseHoldProducts, updateHouseHoldProducts, productStatus, \
    productUpdate, device_details, add_buying_price, manufacture_device_details, add_selling_price, denied_product

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

]
