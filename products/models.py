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
        ('Collected', 'Collected'), ('Requested', 'Requested'),
        ('Pending', 'Pending'), ('Denied', 'Denied'), ('Sold', 'Sold')
    )

    PRO_CATEGORY = (
        ('Published', 'Published'),
        ('Waste', 'Waste')
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

    available_quantity = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    pro_category = models.CharField(max_length=20, choices=PRO_CATEGORY, default=None, null=True)

    # ----------- product pricing ---------------
    payed = models.BooleanField(default=False)
    desired_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    buying_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    # -------product address --------------------
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    sector = models.CharField(max_length=100)
    cell = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    road_number = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=100, null=True, blank=True)

    location_description = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f'{self.product_name}'

    class Meta:
        ordering = ['-created_date']


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


"""model for requested products"""
class RequestedProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(UsersAccount, on_delete=models.SET_NULL, null=True)
    requested_date = models.DateField(auto_now_add=True)
