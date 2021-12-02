from django.db.models import fields
from django.forms import ModelForm
from .models import Product, Address
from userauth.models import UsersAccount


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'product', 'product_image', 'description',
            'quantity', 'cost', 'other', 'user', 'collected_date'
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
            'province', 'sector', 'cell', 'district',
            'village', 'road_number', 'house_number'
            ]


class UpdateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_image', 'description', 'quantity'
            ]