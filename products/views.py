from django import forms
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import status

from .forms import AddProductForm, AddAddressForm, UpdateProductForm, ProductBuyingPriceForm, ProductSellingPriceForm
from .models import Product, Address
from django.core.mail import EmailMessage, send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings

""" View for adding products and address to user"""


def addProduct(request):
    form = AddProductForm(request=request)
    # address_form = AddAddressForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, request=request)
        # address_form = AddAddressForm(request.POST, request.FILES,  request=request)
        # address_form = AddAddressForm(request.POST)
        if form.is_valid():
            # address = address_form.save(commit=False)
            # print(form.cleaned_data['id'])
            # address.user = request.user
            form.save()
            # address.save()

            dat = form.cleaned_data['collected_date']
            device = form.cleaned_data['product_name']

            template = render_to_string('send_email.html', {'name': request.user, 'date': dat})
            template2 = render_to_string('send_email2.html', {'name': request.user, 'device': device, 'date': dat})

            email1 = (
                ' Thanks for adding your product',
                template,
                settings.EMAIL_HOST_USER,
                [request.user.email, 'iradukunda.ta@gmail.com'],
            )
            email2 = (
                ' Thanks for adding your product',
                template2,
                settings.EMAIL_HOST_USER,
                ['iradukunda.ta@gmail.com'],
            )
            send_mass_mail((email1, email2), fail_silently=False)
            # email.fail_silently = False
            # email.send()
            messages.success(request, 'Product Added Successfully')
            return redirect('view_product')
    return render(request, 'addProduct.html', {'form': form})


"""view for viewing the products based on user"""


def houseHoldProducts(request):
    products = Product.objects.filter(user=request.user).order_by('-created_date')
    return render(request, 'houseHoldProducts.html', {'products': products})


"""view for viewing the products based on user"""


def updateHouseHoldProducts(request, id):
    product = get_object_or_404(Product, id=id)
    form = UpdateProductForm(request.POST or None, instance=product)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Updated Successfully')
            return redirect('view_product')
    return render(request, 'houseHoldProductUpdate.html', {'form': form})


"""view for viewing the products based on their status"""


def productStatus(request):
    pending = Product.objects.filter(status='Pending')
    rejected = Product.objects.filter(status='Rejected')
    collected = Product.objects.filter(status='Collected')

    context = {
        'pending': pending,
        'rejected': rejected,
        'collected': collected,
    }

    return render(request, 'productStatus.html', context)


"""view for viewing the products details on Admin side"""


def productUpdate(request, id):
    details = get_object_or_404(Product, id=id)
    address = get_object_or_404(Address, id=id)
    context = {'details': details, 'address': address}
    return render(request, 'productDetails.html', context)


def changeProductToCollected(request, id):
    product = get_object_or_404(Product, id=id)


"""view for viewing the products details"""
def device_details(request, pk):
    details = Product.objects.get(pk=pk)
    context = {'details': details}
    return render(request, 'product_details.html', context)


"""denied products"""
def denied_product(request, pk):
    details = Product.objects.filter(pk=pk).update(status='Denied')
    messages.success(request, 'Successfully denied Product')
    return redirect('dashboard')
    # return render(request, 'product_details.html')


"""view for viewing the products details"""
def manufacture_device_details(request, pk):
    details = Product.objects.get(pk=pk)
    context = {'details': details}
    return render(request, 'dashboard/manufacture_product_details.html', context)


"""view for adding buying price on product"""
def add_buying_price(request, pk):
    product = Product.objects.get(pk=pk)
    form = ProductBuyingPriceForm(request.POST or None, instance=product)
    if request.method == 'POST':
        form = ProductBuyingPriceForm(request.POST or None, instance=product)
        if form.is_valid():
            prod = form.save(commit=False)
            if prod.buying_price > 0:
                prod.payed = True
            else:
                prod.payed = False
            prod.save()
            if prod.buying_price > 0:
                Product.objects.filter(pk=pk).update(status='Collected', pro_category='Published')
            else:
                Product.objects.filter(pk=pk).update(status='Collected', pro_category='Waste')
            messages.success(request, 'Product Buying price Added Successfully')
            return redirect('agent_products')
    context = {'form': form}
    return render(request, 'add_buying_price.html', context)


"""view for adding selling price on product"""
def add_selling_price(request, pk):
    product = Product.objects.get(pk=pk)
    form = ProductSellingPriceForm(request.POST or None, instance=product)
    if request.method == 'POST':
        form = ProductSellingPriceForm(request.POST or None, instance=product)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.save()
            if prod.selling_price > 0:
                Product.objects.filter(pk=pk).update(published=True)
            # else:
            #     Product.objects.filter(pk=pk).update(status='Collected', pro_category='Waste')
            messages.success(request, 'Product selling price Added Successfully')
            return redirect('payed')

    context = {'form': form}
    return render(request, 'add_selling_price.html', context)


"""listing ready for sold products"""
def list_ready_for_sold_products(request):
    data = Product.objects.filter(availability='Available', pro_category='Published')

    """================= snippets for searching ================"""
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.filter(
            Q(category__name__icontains=q) | Q(product_name__icontains=q)
        )
    else:
        data = Product.objects.filter(availability='Available', pro_category='Published')

    p = Paginator(data, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(request, 'ready_sold.html', {'data': data, 'page_obj': page_obj, 'q': q})


"""listing wastes products"""
def list_waste_products(request):
    data = Product.objects.filter(availability='Available', pro_category='Waste')

    """================= snippets for searching ================"""
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.filter(
            Q(category__name__icontains=q) | Q(product_name__icontains=q)
        )
    else:
        data = Product.objects.filter(availability='Available', pro_category='Waste')

    """=================end of snippets for searching ================"""

    p = Paginator(data, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(request, 'waste_product.html', {'data': data, 'page_obj': page_obj, 'q': q})


"""listing published products"""
def list_published_products(request):
    data = Product.objects.filter(availability='Available', published=True)

    """================= snippets for searching ================"""
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.filter(
            Q(category__name__icontains=q) | Q(product_name__icontains=q)
        )
    else:
        data = Product.objects.filter(availability='Available', published=True)

    """=================end of snippets for searching ================"""

    p = Paginator(data, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(request, 'published.html', {'data': data, 'page_obj': page_obj, 'q': q})


"""listing requested products"""
def list_requested_products(request):
    data = Product.objects.filter(availability='Requested')

    """================= snippets for searching ================"""
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.filter(
            Q(category__name__icontains=q) | Q(product_name__icontains=q)
        )
    else:
        data = Product.objects.filter(availability='Requested')

    """=================end of snippets for searching ================"""

    p = Paginator(data, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(request, 'requested_products.html', {'data': data, 'page_obj': page_obj, 'q': q})


"""view for viewing the published details"""
def published_details(request, pk):
    details = Product.objects.get(pk=pk)
    context = {'details': details}
    return render(request, 'published_details.html', context)


"""view for viewing the published details"""
def ready_for_sold_details(request, pk):
    details = Product.objects.get(pk=pk)
    context = {'details': details}
    return render(request, 'ready_sold_details.html', context)