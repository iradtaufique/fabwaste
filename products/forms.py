from django import forms
from django.forms import ModelForm
from .models import Product, Address, RequestedProducts
from userauth.models import UsersAccount


class DateInput(forms.DateInput):
    input_type = 'date'


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'product_name', 'product_image', 'description',
            'quantity', 'desired_price', 'user', 'collected_date', 'district',
            'sector', 'cell', 'village', 'road_number', 'house_number',
        ]

        widgets = {
            'collected_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = UsersAccount.objects.filter(email=self.request.user.email)
        self.fields['user'].empty_label = None


class AddAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = [
            'province', 'district', 'sector', 'cell',
            'village', 'road_number', 'house_number'
        ]


class UpdateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'description', 'quantity', 'availability', 'collected_date',
            'district', 'sector', 'cell', 'village', 'road_number', 'house_number'
        ]

        widgets = {
            'collected_date': DateInput()
        }


class ProductBuyingPriceForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'buying_price', 'available_quantity'
        ]


class ProductSellingPriceForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'selling_price', 'buying_price'
        ]


""" Form for creating requested products """
class RequestedProductForm(ModelForm):
    class Meta:
        model = RequestedProducts
        # fields = '__all__'
        exclude = ['product', 'requested_by']

