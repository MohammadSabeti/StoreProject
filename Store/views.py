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


# INFO: user and accounts func

def login_view(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Successful login
            login(request, user)
            redirect_url = next_url if next_url else reverse('Store:product_list')
            return HttpResponseRedirect(redirect_url)
        else:
            # undefined user or wrong password
            context = {
                'username': username,
                'date_now': datetime.now(),
                'error': 'کاربری با این مشخصات یافت نشد'

            }
    else:
        context = {'date_now': datetime.now()}
    return render(request, 'user/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('Store:login'))


@login_required
def profile_details(request):
    customer = request.user.customer
    context = {
        'customer': customer,
        'date_now': datetime.now()
    }
    return render(request, 'user/profile_details.html', context)


@login_required
def payment_list(request):
    payments = Payment.objects.filter(customer=request.user.customer).order_by('-transaction_time')
    context = {
        'payments': payments,
        'date_now': datetime.now()
    }
    return render(request, 'user/payment_list.html', context)


@login_required
def payment_create(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.profile = request.user.customer
            payment.save()
            request.user.customer.deposit(payment.amount)
            return HttpResponseRedirect(reverse('Store:payment_list'))
    else:
        payment_form = PaymentForm()
    context = {
        'payment_form': payment_form,
        'date_now': datetime.now()
    }
    return render(request, 'user/payment_create.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = MyUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, files=request.FILES, instance=request.user.customer)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('Store:profile_details'))
    else:
        user_form = MyUserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.customer)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'date_now': datetime.now()
    }
    return render(request, 'user/profile_edit.html', context)
