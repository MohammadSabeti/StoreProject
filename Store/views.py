from datetime import datetime

from django.template.loader import render_to_string

from .forms import *
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.

def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'date_now': datetime.now()
    }
    return render(request, 'store/product_list.html', context)


def product_details(request, product_id):
    product = Product.objects.get(pk=product_id)

    context = {
        'product': product,
        'date_now': datetime.now()
    }

    if request.method == 'POST':
        try:
            sell_count = int(request.POST['sell_count'])
            assert product.ProductStatus == product.Available, 'موجودی کالا در انبار به اتمام رسیده است'
            assert product.ProductStock >= sell_count, 'با توجه به موجودی این کالا در انبار در حال حاضر متاسفانه نمی توانیم به این تعداد سفارش پاسخگو باشیم.'
            price = product.ProductPrice * sell_count
            assert request.user.customer.spend(price), 'اعتبار شما برای ثبت سفارش کافی نیست.'
            product.reserve_stock(sell_count)
            order = OrderApp.objects.create(product=product, customer=request.user.customer, sell_count=sell_count)
        except Exception as e:
            context['error'] = str(e)
        else:
            return HttpResponseRedirect(reverse('Store:orderapp_details', kwargs={'orderapp_id': order.id}))
    return render(request, 'store/product_details.html', context)


def orderapp_list(request):
    orderapps = OrderApp.objects.filter(customer_id=request.user.customer).order_by('-order_time')
    context = {
        'orderapps': orderapps,
        'date_now': datetime.now()

    }
    return render(request, 'store/orderapp_list.html', context)


def orderapp_details(request, orderapp_id):
    orderapp = OrderApp.objects.get(pk=orderapp_id)
    context = {
        'orderapp': orderapp,
        'date_now': datetime.now()
    }
    return render(request, 'store/orderapp_details.html', context)
