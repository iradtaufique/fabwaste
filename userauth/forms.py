from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm, fields
from .models import UsersAccount, Profile
from django.contrib.auth.forms import AuthenticationForm


class RegisterUserForm(ModelForm):
    full_name = forms.CharField(label='FullName', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',
                             error_messages={'required': 'Sorry, you will need an email'})
    mobile = forms.CharField(label='Phone Number', min_length=10, max_length=13)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UsersAccount
        fields = ['full_name', 'email', 'mobile', 'location']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password Do not match!!')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UsersAccount.objects.filter(email=email).exists():
            raise forms.ValidationError('Email olready Taken')
        return email

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['full_name'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Your Full Name'})
    #     self.fields['email'].widget.attrs.update({'class': 'form-control mb-3', 'name': 'email', 'placeholder': 'Email'})
    #     self.fields['password'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Password'})
    #     self.fields['password2'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password', 'id': 'login-pwd'}))


"""new form for loging user"""


class LoginUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UsersAccount
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Check your username or password if are correct')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
