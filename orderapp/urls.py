from django.urls import path

from orderapp.views import order_create, not_product, not_money


app_name = 'orderapp'

urlpatterns = [
    path('create/', order_create, name='create'),
    path('not-items/<int:prod_id>', not_product, name='not_product'),
    path('not-money/', not_money, name='not_money')
    ]
