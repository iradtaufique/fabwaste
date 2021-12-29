import datetime

from django.db import models
from django.db.models.fields.related import ForeignKey
from userauth.models import UsersAccount, District
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    minimum_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    maximum_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)


class Product(models.Model):
    AVAILABILITY = (
        ('Available', 'Available'),
        ('UnAvailable', 'UnAvailable'),
    )
    STATUS = (
        ('Collected', 'Collected'),
        ('Pending', 'Pending'), ('Denied', 'Denied'),
    )

    user = models.ForeignKey(UsersAccount, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='media')
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    collected_date = models.DateField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    availability = models.CharField(max_length=20, choices=AVAILABILITY, default='Available')

    # ----------- product pricing ---------------
    payed = models.BooleanField(default=False)
    desired_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    buying_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    # -------product address --------------------
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING)
    sector = models.CharField(max_length=100)
    cell = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    road_number = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.product_name}'


class Address(models.Model):
    user = models.ForeignKey(UsersAccount, on_delete=models.DO_NOTHING, default=None)
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    cell = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    road_number = models.CharField(max_length=10)
    house_number = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.province}'
