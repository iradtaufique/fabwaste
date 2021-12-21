from django.contrib import admin
from userauth.models import Profile, UsersAccount, District

# Register your models here.
admin.site.register(Profile)
admin.site.register(UsersAccount)
admin.site.register(District)
