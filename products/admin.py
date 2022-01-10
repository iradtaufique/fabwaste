from django.contrib import admin
from .models import Product, Category, Address, RequestedProducts

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(RequestedProducts)
