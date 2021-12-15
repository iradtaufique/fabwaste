from django.urls import path
from .views import RegisterUserAPi, UserLoginApiView, CreateProductApiView, ListDevicesApiView, ListUsersApiView, \
    RegisterAgentAPiView, RegisterHouseHoldAPiView, ListHouseHoldPayedProductApiView

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
    path('register/', RegisterUserAPi.as_view(), name='register'),
    path('register-agent/', RegisterAgentAPiView.as_view(), name='register_agent'),
    path('register-house-hold/', RegisterHouseHoldAPiView.as_view(), name='register_house_hold'),
    path('login_user/', UserLoginApiView.as_view(), name='login_user'),
    path('create-product/', CreateProductApiView.as_view(), name='create_product'),
    path('list-product/', ListDevicesApiView.as_view(), name='list_devices'),
    path('list-household-payed-product/', ListHouseHoldPayedProductApiView.as_view(), name='list_household_payed_product'),
    path('list-users/', ListUsersApiView.as_view(), name='list_users'),

    # documentation links
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
