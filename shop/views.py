from urllib.parse import urlencode

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from shop.models import Product, Category


def index(request):
    page = request.GET.get('page')
    category = request.GET.get('category')
    name = request.GET.get('name')

    queryset = Product.objects.all()

    if name:
        queryset = queryset.filter(name__contains=name)

    if category and int(category) > -1:
        queryset = queryset.filter(category=category)

    paginator = Paginator(queryset, 10)
    products = paginator.get_page(page)
    template = loader.get_template('home.html')

    gt = request.GET.copy()
    if 'page' in gt:
        del gt['page']

    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'pages': range(paginator.num_pages),
        'params': urlencode(gt),
    }
    return HttpResponse(template.render(context, request))


def cart(request):
    template = loader.get_template('cart.html')
    context = {}
    return HttpResponse(template.render(context, request))
