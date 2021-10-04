from django.urls import path

from purse.views import AddWalletView
app_name = 'purse'


urlpatterns = [
    path('add_money/', AddWalletView.as_view(), name='money')
]
