from django.urls import path

from shopapp.views import ShowProduct, CategoryProduct, ProductDetail


app_name = 'shopapp'


urlpatterns = [
               path('catalog/', ShowProduct.as_view(), name='catalog'),
               path('catalog/<slug:slug_cat>/', CategoryProduct.as_view(), name='categories'),
               path('catalog/<slug:slug_cat>/<slug:slug>/', ProductDetail.as_view(), name='product')

]
