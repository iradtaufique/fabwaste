from django.forms import ModelForm
from products.models import Category, SubCategory


class AddCategoriesForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class AddSubCategoriesForm(ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'
