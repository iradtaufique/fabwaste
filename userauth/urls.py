from django.urls import path
from .views import home, register, loginUser, account_activate, register_agent, register_manufacture
from django.contrib.auth import views
from .forms import UserLoginForm
from .views import loginUser
urlpatterns = [
    # path('', home, name='home'),
    path('register-user', register, name='register_user'),
    path('register-agent', register_agent, name='register_agent'),
    path('register-manufacture', register_manufacture, name='register_manufacture'),
    path('', views.LoginView.as_view(template_name='registration/login.html', form_class=UserLoginForm), name='user_login'),
    path('logout/', views.LogoutView.as_view(next_page='user_login'), name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate'),
]
