from datetime import datetime
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from shop.models import Product, Category, ProductsInCart, Order


@login_required
def add_to_cart(request, product_id):
    user_cart = request.user.cart

    found_products = user_cart.products.filter(product_id=product_id)
    if len(found_products) > 0:
        for product_in_cart in found_products:
            product_in_cart.quantity += 1
            product_in_cart.save()
    else:
        product_in_cart = ProductsInCart(product_id=product_id)
        product_in_cart.save()

        user_cart.products.add(product_in_cart)
        request.user.save()

    messages.success(request, 'Product successfully added to cart.')

    return redirect('home')


@login_required
def remove_from_cart(request, product_id):
    user_cart = request.user.cart

    for product_in_cart in user_cart.products.all():
        if product_in_cart.product.pk == product_id:
            user_cart.products.remove(product_in_cart)
            break

    return redirect('cart')


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


def calculate_total_cart_cost(user_cart):
    total_card_cost = 0

    for product_in_cart in user_cart.products.all():
        total_card_cost += product_in_cart.line_total()

    return total_card_cost


def cart(request):
    user_cart = request.user.cart
    template = loader.get_template('cart.html')
    context = {'total_cost': calculate_total_cart_cost(user_cart)}
    return HttpResponse(template.render(context, request))


def checkout(request):
    user_cart = request.user.cart

    new_order = Order(order_date=datetime.now(),
                      user_id=request.user.id,
                      delivery_detiles=request.user.delivery_address,
                      cost=calculate_total_cart_cost(user_cart)
                      )

    new_order.save()

    for product_in_cart in user_cart.products.all():
        new_order.products.add(product_in_cart.product.pk)
        user_cart.products.remove(product_in_cart)

    messages.success(request, 'Order successfully created.')

    return redirect('cart')
