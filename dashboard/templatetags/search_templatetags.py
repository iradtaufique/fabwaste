from django.db.models import Q
from django.shortcuts import render
from django import template

register = template.Library()
from products.models import Product


@register.simple_tag
def search(request):
    q = ''
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.filter(
            Q(category__name__icontains=q) | Q(product_name__icontains=q)
        )
    else:
        data = Product.objects.all()

    return render(request, {'data': data})
