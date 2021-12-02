import datetime

from django.db import models
from django.db.models.fields.related import ForeignKey
from userauth.models import UsersAccount
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    cost = models.CharField(max_length=30, default=0)

    def __str__(self):
        return f'{self.name}'

# Create your models here.
class Product(models.Model):
    # COST = (
    #     ('5000-10000', '5000-10000'),
    # )
    STATUS = (
        ('Pending', 'Pending'), ('Collected', 'Collected'),
        ('Rejected', 'Rejected')
    )
    user = models.ForeignKey(UsersAccount, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    product_image = models.ImageField(upload_to='media')
    description = models.TextField()
    created_date = models.DateField(auto_now=True)
    collected_date = models.DateField(default=timezone.now)
    quantity = models.IntegerField()
    cost = models.CharField(max_length=20)
    other = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')


class Address(models.Model):
    user = models.ForeignKey(UsersAccount, on_delete=models.DO_NOTHING)
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    cell = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    road_number = models.CharField(max_length=10)
    house_number = models.CharField(max_length=10)