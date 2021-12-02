from django.urls import path
from .views import addProduct, houseHoldProducts, updateHouseHoldProducts, productStatus,\
            productDetails


urlpatterns = [
    path('add-product', addProduct, name='add_product'),
    path('view-product', houseHoldProducts, name='view_product'),
    path('view-product/<int:id>', updateHouseHoldProducts, name='view_product_details'),
    path('pending-product', productStatus, name='pending'),
    path('rejected-product', productStatus, name='rejected'),
    path('collected-product', productStatus, name='collected'),
    path('details/<int:id>/', productDetails, name='details'),

]
