from django.urls import path
from .views import RegisterUserAPi, UserLoginApiView, CreateProductApiView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('register/', RegisterUserAPi.as_view(), name='register'),
    path('login_user/', UserLoginApiView.as_view(), name='login_user'),
    path('create-product/', CreateProductApiView.as_view(), name='create_product'),

    # documentation links
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]
