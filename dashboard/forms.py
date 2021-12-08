from django.forms import ModelForm
from products.models import Category


class AddCategoriesForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
