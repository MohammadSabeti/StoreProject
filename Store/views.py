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

