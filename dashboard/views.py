from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from userauth.models import UsersAccount
from products.models import Product, Category, Address
from .forms import AddCategoriesForm, AddSubCategoriesForm
from django.contrib import messages


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


@login_required
def index(request):
    total_users = UsersAccount.objects.all().exclude(is_superuser=True).count()
    # house_hold_unsold_products = Product.objects.filter(user=request.user, status='UnSold')
    house_hold_unsold_products = Product.objects.filter(user=request.user)
    total_collected_devices = Product.objects.filter(status='Collected').count()
    household_total_devices = Product.objects.filter(user=request.user).count()
    household_earned_money = Product.objects.filter(user=request.user, payed=True)
    household_picked_device = Product.objects.filter(user=request.user, status='Collected').count()
    household_sold_device = Product.objects.filter(user=request.user, status='Collected', payed=True).count()
    total_unpayed_devices = Product.objects.filter(payed=False, status='Collected').count()
    total_payed_devices = Product.objects.filter(payed=True).count()

    money = 0

    for i in household_earned_money:
        money = money + i.buying_price

    context = {
        'total_users': total_users,
        'total_collected_devices': total_collected_devices,
        'total_payed_devices': total_payed_devices,
        'total_unpayed_devices': total_unpayed_devices,
        'household_total_devices': household_total_devices,
        'household_picked_device': household_picked_device,
        'household_sold_device': household_sold_device,
        'money': money,
        'devices': house_hold_unsold_products,

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
    categories = Category.objects.all()
    form = AddCategoriesForm()
    if request.method == 'POST':
        form = AddCategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Added Successfully')
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'dashboard/add_categories.html', context)


# ------------- view for deleting user ------------
def delete_user(request, id):
    data = UsersAccount.objects.get(id=id)
    if request.method == 'POST':
        data.delete()
        return redirect('list_user')
    return render(request, 'dashboard/delete_user.html')


# --------- view for near agents on household ---------
def near_agent_view(request):
    agents = UsersAccount.objects.filter(is_agent=True, location=request.user.location)
    context = {
        'agents': agents,
    }
    return render(request, 'dashboard/household_near_agent.html', context)


# def house_hold_update_product(request, pk):
#     update = Product.objects.get(pk=pk)
#     form =
#     context = {'update': update}
#     return render(request, 'dashboard/house_hold_update_product.html', context)

def add_sub_category(request):
    form = AddSubCategoriesForm()
    if request.method == 'POST':
        form = AddSubCategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_sub_category.html', context)
