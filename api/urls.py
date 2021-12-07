from django.urls import path
from .views import RegisterUserAPi, UserLoginApiView, CreateProductApiView

urlpatterns = [
    path('register/', RegisterUserAPi.as_view(), name='register'),
    path('login_user/', UserLoginApiView.as_view(), name='login_user'),
    path('create-product/', CreateProductApiView.as_view(), name='create_product'),
]