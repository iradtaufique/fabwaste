from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from userauth.forms import RegisterUserForm
from .models import UsersAccount
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .tokens import account_activation_token


def home(request):
    return render(request, 'base.html')


def register(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.full_name = form.cleaned_data['full_name']
            user.mobile = form.cleaned_data['mobile']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Account'
            message = render_to_string(
                'registration/account_activation _email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),

            })
            user.email_user(subject=subject, message=message)
            return render(request, 'registration/register_email_confirm.html')
        else:
            form = RegisterUserForm()
    return render(request, 'registration/register.html', {'form': form})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UsersAccount.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_house_hold = True
        user.save()
        login(request, user)

        a = UsersAccount.objects.get(email=request.user.email)
        # for i in a:
        #     nam = i.full_name
        messages.success(request, "Welcome " + a.full_name + " Your Account has been activated")
        return redirect('home')
    else:
        return render(request, 'registration/activation_invalid.html')


def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username of Password incorrect')
    return render(request, 'registration/login.html')