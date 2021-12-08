from django.shortcuts import render, redirect, get_object_or_404
from userauth.models import UsersAccount
from products.models import Product, Category, Address
from .forms import AddCategoriesForm


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def index(request):
    total_users = UsersAccount.objects.all().exclude(is_superuser=True).count()
    total_collected_devices = Product.objects.filter(status='Collected').count()
    total_unpayed_devices = Product.objects.filter(payed=False, availability='Available', status='Collected').count()
    total_payed_devices = Product.objects.filter(payed=True).count()
    context = {
        'total_users': total_users,
        'total_collected_devices': total_collected_devices,
        'total_payed_devices': total_payed_devices,
        'total_unpayed_devices': total_unpayed_devices,

    }
    return render(request, 'dashboard/index.html', context)


def payed_devices(request):
    devices = Product.objects.filter(payed=True)
    context = {
        'devices': devices,
    }
    return render(request, 'dashboard/payed_devices.html', context)


def un_payed_devices(request):
    devices = Product.objects.filter(payed=False).exclude(status='Collected')
    context = {
        'devices': devices,
    }
    return render(request, 'dashboard/not_payed_devices.html', context)


def un_available_devices(request):
    devices = Product.objects.filter(availability='Not_Available')
    context = {
        'devices': devices,
    }
    return render(request, 'dashboard/unvailable.html', context)


"""available devices to be collected"""


def available_devices(request):
    devices = Product.objects.filter(availability='Available').exclude(status='Collected')
    context = {
        'devices': devices,
    }
    return render(request, 'dashboard/available.html', context)


def user_list(request):
    users_list = UsersAccount.objects.all().exclude(is_superuser=True)
    context = {
        'users_list': users_list
    }
    return render(request, 'dashboard/users_list.html', context)


def add_categories(request):
    form = AddCategoriesForm()
    if request.method == 'POST':
        form = AddCategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_categories.html', context)


def delete_user(request, id):
    data = UsersAccount.objects.get(id=id)
    if request.method == 'POST':
        data.delete()
        return redirect('list_user')
    return render(request, 'dashboard/delete_user.html')

