from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from .forms import AddProductForm, AddAddressForm, UpdateProductForm
from .models import Product, Address
from django.core.mail import EmailMessage, send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings

""" View for adding products and address to user"""


def addProduct(request):

    form = AddProductForm(request=request)
    address_form = AddAddressForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, request=request)
        # address_form = AddAddressForm(request.POST, request.FILES,  request=request)
        address_form = AddAddressForm(request.POST)
        if form.is_valid() and address_form.is_valid():
            address = address_form.save(commit=False)
            # print(form.cleaned_data['id'])
            address.user = request.user
            form.save()
            address.save()

            dat = form.cleaned_data['collected_date']
            device = form.cleaned_data['product']

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
            return redirect('view_product')
    return render(request, 'addProduct.html', {'form': form, 'address_form': address_form})


"""view for viewing the products based on user"""
def houseHoldProducts(request):
    products = Product.objects.filter(user=request.user)
    if request.user.is_staff:
        products = Product.objects.all()
    return render(request, 'houseHoldProducts.html', {'products': products})


"""view for viewing the products based on user"""


def updateHouseHoldProducts(request, id):
    product = get_object_or_404(Product, id=id)
    form = UpdateProductForm(request.POST or None, instance=product)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
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