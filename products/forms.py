from django.db.models import fields
from django.forms import ModelForm
from .models import Product, Address
from userauth.models import UsersAccount


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name', 'product_image', 'description',
            'quantity', 'price', 'other', 'user', 'collected_date'
            ]

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
            'product_image', 'description', 'quantity'
            ]