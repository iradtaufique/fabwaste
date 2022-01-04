from django.urls import path
from .views import home, register, loginUser, account_activate, register_agent, register_manufacture, UserLoginn, \
    user_profile, edit_user_profile
from django.contrib.auth import views
from .forms import UserLoginForm
from django.contrib.auth import views as auth_views
from .views import loginUser


urlpatterns = [
    # path('', home, name='home'),
    path('register-user', register, name='register_user'),
    path('register-agent', register_agent, name='register_agent'),
    path('register-manufacture', register_manufacture, name='register_manufacture'),
    path('', views.LoginView.as_view(template_name='registration/login.html', form_class=UserLoginForm), name='user_login'),
    path('logout/', views.LogoutView.as_view(next_page='user_login'), name='logout'),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('user-profile/', user_profile, name='user_profile'),
    path('edit-user-profile/<int:pk>', edit_user_profile, name='edit_user_profile'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate'),
    # path('login/', UserLoginn, name='user_login'),
]
