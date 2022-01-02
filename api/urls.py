from django.urls import path
from .views import RegisterUserAPi, UserLoginApiView, CreateProductApiView, ListDevicesApiView, ListUsersApiView, \
    RegisterAgentAPiView, RegisterHouseHoldAPiView, ListHouseHoldPayedProductApiView, ListAllAgentAPIView, \
    ListElectronicsProductsApiView, ListPlasticsProductsApiView, ListMetalsProductsApiView, ListTextileProductsApiView, \
    RegisterManufactureAPiView, ProductDetailsAPIView, AgentDetailsAPIView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Fab|Waste API",
      default_version='v1',
      description="Fab Waste API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('register/', RegisterUserAPi.as_view(), name='register_api'),
    path('register-agent/', RegisterAgentAPiView.as_view(), name='register_agent_api'),
    path('register-manufacture/', RegisterManufactureAPiView.as_view(), name='register_manufacture_api'),
    path('register-house-hold/', RegisterHouseHoldAPiView.as_view(), name='register_house_hold_api'),
    path('login_user/', UserLoginApiView.as_view(), name='login_user_api'),
    path('create-product/', CreateProductApiView.as_view(), name='create_product_api'),
    path('list-product/', ListDevicesApiView.as_view(), name='list_devices_api'),
    path('product/<int:pk>', ProductDetailsAPIView.as_view(), name='list_product_details_api'),

    path('list-household-payed-product/', ListHouseHoldPayedProductApiView.as_view(), name='list_household_payed_product_api'),
    path('list-users/', ListUsersApiView.as_view(), name='list_users'),
    path('list-agents-api/', ListAllAgentAPIView.as_view(), name='list_agents_api'),
    path('agent/<int:pk>', AgentDetailsAPIView.as_view(), name='agent_details_api'),
    path('electronic-products-api/', ListElectronicsProductsApiView.as_view(), name='electronic_product_api'),
    path('plastic-products-api/', ListPlasticsProductsApiView.as_view(), name='plastics_product_api'),
    path('metal-products-api/', ListMetalsProductsApiView.as_view(), name='metals_product_api'),
    path('textile-products-api/', ListTextileProductsApiView.as_view(), name='textile_product_api'),

    # documentation links
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
