from django.urls import path
from .views import (dashboard, index, payed_devices, un_payed_devices,
                    un_available_devices, user_list)


urlpatterns = [

    # path('', dashboard, name='dashboard'),
    path('', index, name='dashboard'),
    path('payed-devices', payed_devices, name='payed'),
    path('un-payed_', un_payed_devices, name='un_payed'),
    path('un-available', un_available_devices, name='un_available'),
    path('user-list', user_list, name='list_user'),
]
