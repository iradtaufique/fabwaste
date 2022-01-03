from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from userauth.models import UsersAccount
from products.models import Product, Category, Address, SubCategory
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
    agent_total_devices = Product.objects.filter(availability='Available', status='Pending').count()

    # categories = Category.objects.all()
    categ = []
    cateName = []

    categories = Category.objects.all()

    for i in categories:
        categ.append(i.id)
        cateName.append(i.name)
    print(categ)
    print(cateName)
    """================= snippets for searching ================"""
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.filter(
            Q(category__name__icontains=q) | Q(product_name__icontains=q)
        )
    else:
        data = Product.objects.all()

    """=================end of snippets for searching ================"""

    """=================end of snippets for pagination ================"""
    p = Paginator(data, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    """=================end of snippets for pagination ================"""

    total_textile_products = Product.objects.filter(category__name='Textile', status='Collected').count()
    total_electronics_products = Product.objects.filter(category__name='Electronics', status='Collected').count()
    total_metals_products = Product.objects.filter(category__name='Metals', status='Collected').count()
    total_plastics_products = Product.objects.filter(category__name='Plastics', status='Collected').count()
    agent_total_collected_devices = Product.objects.filter(status='Collected').count()
    agent_total_denied_devices = Product.objects.filter(status='Denied').count()
    agent_total_payed_devices = Product.objects.filter(status='Collected', payed=True).count()
    agent_total_unpayed_devices = Product.objects.filter(status='Collected', payed=False).count()
    agent_total_users = UsersAccount.objects.filter(location=request.user.location).count()

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
        'categories': categories,
        'total_textile_products': total_textile_products,
        'total_metals_products': total_metals_products,
        'total_plastics_products': total_plastics_products,
        'total_electronics_products': total_electronics_products,
        'agent_total_devices': total_electronics_products,
        'agent_total_collected_devices': agent_total_collected_devices,
        'agent_total_denied_devices': agent_total_denied_devices,
        'agent_total_payed_devices': agent_total_payed_devices,
        'agent_total_unpayed_devices': agent_total_unpayed_devices,
        'agent_total_users': agent_total_users,
        'data': data,
        'page_obj': page_obj,

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
            form = AddCategoriesForm()
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


def add_sub_category(request):
    form = AddSubCategoriesForm()
    if request.method == 'POST':
        form = AddSubCategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sub category added Successfully!')
            return redirect('view_subcategory')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_sub_category.html', context)


def view_textile_products(request):
    textile = Product.objects.filter(category__name='Textile', status='Collected')
    context = {
        'textile': textile,
    }
    return render(request, 'dashboard/textile_products.html', context)


def view_electronics_products(request):
    electronics = Product.objects.filter(category__name='Electronics', status='Collected')
    context = {
        'electronics': electronics,
    }
    return render(request, 'dashboard/electronics_products.html', context)


def view_metals_products(request):
    metals = Product.objects.filter(category__name='Metals', status='Collected')
    context = {
        'metals': metals,
    }
    return render(request, 'dashboard/metals_product.html', context)


def view_plastics_products(request):
    plastics = Product.objects.filter(category__name='Plastics', status='Collected')
    context = {
        'plastics': plastics,
    }
    return render(request, 'dashboard/plastics_products.html', context)


"""view for viewing products which are on agent location"""
def agent_view_products(request):
    data = Product.objects.filter(district=request.user.location, availability='Available', status='Pending')
    return render(request, 'dashboard/agent_products.html', {'data': data})


"""view for viewing products which are on agent location"""
def agent_view_collected_products(request):
    data = Product.objects.filter(district=request.user.location, status='Collected')
    return render(request, 'dashboard/agent_collected_products.html', {'data': data})


"""view for viewing users which are on agent location"""
def agent_view_users(request):
    data = UsersAccount.objects.filter(location=request.user.location, is_house_hold=True)
    return render(request, 'dashboard/agent_users.html', {'data': data})


"""view for viewing subcategories on agent side"""
def agent_view_subcategories(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'dashboard/list_subcategories.html', {'subcategories': subcategories})


"""view for viewing subcategories on admin side"""
def view_subcategories(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'dashboard/admin_list_subcategories.html', {'subcategories': subcategories})


"""view for editing subcategory"""
def edit_sub_category(request, pk):
    data = get_object_or_404(SubCategory, id=pk)
    form = AddSubCategoriesForm(instance=data)
    if request.method == 'POST':
        form = AddSubCategoriesForm(request.POST or None, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sub category edited Successfully!')
            return redirect('view_subcategory')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_sub_category.html', context)


"""view for deleting subcategory"""
def delete_subcategory(request, pk):
    data = get_object_or_404(SubCategory, id=pk)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Item Deleted Successfully')
        return redirect('view_subcategory')
    return render(request, 'dashboard/delete.html')
