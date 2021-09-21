import hashlib
from datetime import date
from random import random

from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
    forms,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm)
from django.utils.translation import gettext_lazy as _

from .models import User, UserProfile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User  # модель пользователя
        fields = ['email', 'password']  # поля используемые для аунтификации

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # задаем стиль


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'birthday']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # Проверка возраста, при возрасте меньше 18 вызывается ошибка
    def clea_age(self):
        birthday = self.cleaned_data['birthday']
        today = date.today()
        data = today.year - birthday.year - (
                (today.month, today.day) < (birthday.month, birthday.day))
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')

        return data

    def save(self, *args, **kwargs):
        user = super(UserRegisterForm, self).save()

        user.is_activate = False
        salt = hashlib.sha1(
            str(random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'birthday']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clea_age(self):
        birthday = self.cleaned_data['birthday']
        today = date.today()
        data = today.year - birthday.year - (
                (today.month, today.day) < (birthday.month, birthday.day))
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')

        return data


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'avatar', 'region', 'phone']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PasswordReset(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )


class SetPassword(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class ChangePassword(SetPassword, PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}),
    )
