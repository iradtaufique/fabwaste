from django.urls import path
from .views import (available_devices, index, payed_devices, un_payed_devices,
                    un_available_devices, user_list, add_categories, delete_user, near_agent_view, add_sub_category,
                    view_textile_products, view_electronics_products, view_metals_products, view_plastics_products,
                    agent_view_products, agent_view_users, agent_view_subcategories, agent_view_collected_products,
                    view_subcategories, edit_sub_category, delete_subcategory)


urlpatterns = [

    path('', index, name='dashboard'),
    path('payed-devices', payed_devices, name='payed'),
    path('un-payed', un_payed_devices, name='un_payed'),
    path('available-devices', available_devices, name='available_devices'),
    path('un-available', un_available_devices, name='un_available'),
    path('user-list', user_list, name='list_user'),
    path('add-category', add_categories, name='add_category'),
    path('add-sub-category', add_sub_category, name='add_sub_category'),
    path('textile-products', view_textile_products, name='textile_products'),
    path('electronics-products', view_electronics_products, name='electronics_products'),
    path('metals-products', view_metals_products, name='metals_products'),
    path('plastics-products', view_plastics_products, name='plastics_products'),
    path('agent-products', agent_view_products, name='agent_products'),
    path('agent-collected-products', agent_view_collected_products, name='agent_collected_products'),
    path('agent-users', agent_view_users, name='agent_users'),
    path('delete-user/<int:id>', delete_user, name='delete_user'),
    path('agent-subcategories', agent_view_subcategories, name='agent_subcategory'),
    path('view-subcategories', view_subcategories, name='view_subcategory'),
    path('edit-subcategories/<int:pk>', edit_sub_category, name='edit_subcategory'),
    path('delete-subcategories/<int:pk>', delete_subcategory, name='delete_subcategory'),

    # ---- urls for household ------------
    path('nearest-agent', near_agent_view, name='near_agent')
]
