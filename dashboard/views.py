from django.shortcuts import render
from userauth.models import UsersAccount
from products.models import Product, Category, Address


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def index(request):
    total_users = UsersAccount.objects.all().exclude(is_superuser=True).count()
    total_collected_devices = Product.objects.filter(status='Collected').count()
    total_devices = Product.objects.filter(availability='Available', status='Collected').count()
    total_payed_devices = Product.objects.filter(payed=True).count()
    context = {
        'total_users': total_users,
        'total_collected_devices': total_collected_devices,
        'total_payed_devices': total_payed_devices,
        'total_devices': total_devices,

    }
    return render(request, 'dashboard/index.html', context)


def payed_devices(request):
    return render(request, 'dashboard/payed_devices.html')


def un_payed_devices(request):
    return render(request, 'dashboard/not_payed_devices.html')


def un_available_devices(request):
    return render(request, 'dashboard/unvailable.html')


def user_list(request):
    return render(request, 'dashboard/users_list.html')