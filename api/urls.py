from django.urls import path
from .views import RegisterUserAPi

urlpatterns = [
    path('register/', RegisterUserAPi.as_view(), name='register'),
]