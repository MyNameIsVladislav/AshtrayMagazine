from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)

from .views import *


app_name = 'authapp'

urlpatterns = [
               path('login/', login, name='login'),
               path('logout/', logout, name='logout'),
               path('register/', register, name='register'),
               path('edit/user/', edit_user, name='edit'),
               path('edit/profile/', edit_profile, name='profile'),
               path('verify/<str:email>/<str:activation_key>', verify, name='verify'),
               path('password-change/', PassChangeView.as_view(), name='password_change'),
               path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
               path('password-reset/', PassResetView.as_view(), name='password_reset'),
               path('password-reset/done/', PasswordResetDoneView.as_view(),
                    name='password_reset_done'),
               url(r'password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', PassResetConfirmView.as_view(),
                   name='password_reset_confirm'),
               path('password-reset/complete/', PasswordResetCompleteView.as_view(),
                    name='password_reset_complete')
               ]
