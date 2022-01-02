from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, full_name, password,  **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, full_name, password,  **other_fields)

    def create_user(self, email, full_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class UsersAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email Address', unique=True)
    full_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=12, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_house_hold = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_manufacture = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    location = models.ForeignKey(District, on_delete=models.DO_NOTHING, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(UsersAccount, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(default='blank-person.jpg')
    sector = models.CharField(max_length=100, null=True, blank=True)
    cell = models.CharField(max_length=100, null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)
