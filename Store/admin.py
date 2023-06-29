from django.contrib import admin
from Store.models import *
from Store.models import OrderApp

admin.site.register(OrderApp)
admin.site.register(Payment)
