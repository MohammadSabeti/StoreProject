from django.urls import path
from Store import views
app_name = 'Store'
urlpatterns = [
    path('product/list/', views.product_list, name='product_list'),
    path('product/details/<int:product_id>/', views.product_details, name='product_details'),
    path('orderapp/list/', views.orderapp_list, name='orderapp_list'),
    path('orderapp/details/<int:orderapp_id>/', views.orderapp_details, name='orderapp_details'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/details/', views.profile_details, name='profile_details'),
    path('payment/list/', views.payment_list, name='payment_list'),
    path('payment/create/', views.payment_create, name='payment_create'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]