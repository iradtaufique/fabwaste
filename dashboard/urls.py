from django.urls import path
from .views import (available_devices, index, payed_devices, un_payed_devices,
                    un_available_devices, user_list, add_categories, delete_user)


urlpatterns = [

    path('', index, name='dashboard'),
    path('payed-devices', payed_devices, name='payed'),
    path('un-payed_', un_payed_devices, name='un_payed'),
    path('available-devices', available_devices, name='available_devices'),
    path('un-available', un_available_devices, name='un_available'),
    path('user-list', user_list, name='list_user'),
    path('add-category', add_categories, name='add_category'),
    path('delete-user/<int:id>', delete_user, name='delete_user'),
]
