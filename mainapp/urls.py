from django.urls import path

from .views import index, contact

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contact, name='contact')
]
