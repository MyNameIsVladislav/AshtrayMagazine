from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)

from core import settings
from authapp.forms import (
    UserEditForm,
    UserRegisterForm,
    UserLoginForm,
    EditProfileForm,
    ChangePassword,
    PasswordReset,
    SetPassword
)
from authapp.models import User
from authapp.utils.functions.send_mail import send_verify_mail

profile_menu = [
    {'title': 'Аккаунт', 'url': 'edit', 'namespace': 'auth:edit'},
    {'title': 'Личные данные', 'url': 'profile', 'namespace': 'auth:profile'}
]


def login(request):
    title = _('Enter')
    if request.GET.get('next'):
        messages.add_message(request, messages.INFO, "Ваши действия требуют авторизации")

    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        email = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))

    content = {'title': title, 'login_form': login_form}
    return render(request, 'registration/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    title = _('Registration')

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = UserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'registration/register.html', content)


def edit_user(request):
    title = _('Account')
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = UserEditForm(instance=request.user)
        content = {'title': title, 'edit_form': edit_form, 'menu': profile_menu, 'namespace': 'auth:edit'}

        return render(request, 'registration/edit.html', content)


def edit_profile(request):
    title = _('Profile')
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('auth:profile'))

    profile_form = EditProfileForm(instance=request.user.userprofile)
    content = {'title': title, 'edit_form': profile_form, 'menu': profile_menu, 'namespace': 'auth:profile'}
    return render(request, 'registration/edit.html', content)


def verify(request, email, activation_key):
    user = User.objects.get(email=email)
    if user.activation_key == activation_key and not user.is_activation_key_expired():
        user.is_active = True
        user.save()
        auth.login(request, user)
        return render(request, 'registration/verification.html')
    else:
        print(f'error activation user: {user}')
        return render(request, 'registration/verification.html')


class PassChangeView(PasswordChangeView):
    success_url = reverse_lazy('auth:password_change_done')
    form_class = ChangePassword


class PassResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy('auth:password_reset_done')
    from_email = settings.EMAIL_HOST_USER
    form_class = PasswordReset


class PassResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('auth:password_reset_complete')
    form_class = SetPassword
