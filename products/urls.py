from django.urls import path
from .views import addProduct, houseHoldProducts, updateHouseHoldProducts, productStatus,\
            productUpdate, device_details


urlpatterns = [
    path('add-product', addProduct, name='add_product'),
    path('view-product', houseHoldProducts, name='view_product'),
    path('view-product/<int:id>', updateHouseHoldProducts, name='update_product'),
    path('pending-product', productStatus, name='pending'),
    path('rejected-product', productStatus, name='rejected'),
    path('collected-product', productStatus, name='collected'),
    path('update/<int:id>/', productUpdate, name='product_update'),
    path('device-details/<int:pk>/', device_details, name='device_details'),

]
