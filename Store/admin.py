from django.contrib import admin
from Store.models import *
from Store.models import OrderApp


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'mobile', 'get_balance_display')
    list_filter = ('address', 'gender')
    search_fields = ('user__username',)
    ordering = ['pk']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('ProductName', 'ProductStock', 'ProductStatus', 'get_price_display')
    list_filter = ('ProductStatus',)
    search_fields = ('ProductName',)
    ordering = ['pk']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderApp)
admin.site.register(Payment)
