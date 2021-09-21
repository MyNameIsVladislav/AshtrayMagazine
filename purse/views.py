from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import PermissionRequiredMixin

from purse.forms import AddMoneyForm
from purse.models import PurseModel
from core.settings import EMAIL_HOST_USER


MESSAGE_FOR_MAIL = """
Ваш баланс успешно пополнен на {} рублей.
На вашем счете {} рублей.

{}, хорошего дня и приятных покупок в AshtrayMagazine!
"""


class AddWalletView(TemplateView, RedirectView):
    # permission_required = ('purse.can_add_money', 'purse.can_edit')

    template_name = 'wallet/add_money.html'

    def get_context_data(self, **kwargs):
        context = super(AddWalletView, self).get_context_data(**kwargs)
        context['form_for_money'] = AddMoneyForm()
        return context

    def get(self, request, *args, **kwargs):
        if kwargs.get('message', None):
            messages.add_message(request, messages.INFO, "Баланс успешно пополнен")
        return super(AddWalletView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_wallet = PurseModel.objects.get_or_create(user_id=cd['user_id'])[0]
            user_wallet.money += cd['money']
            user_wallet.save()

            message = MESSAGE_FOR_MAIL.format(cd['money'], user_wallet.money, user_wallet.full_name)

            send_mail(
                'Полнение баланса',
                message,
                EMAIL_HOST_USER,
                [user_wallet.user_id.email]
            )
            kwargs['message'] = True
            return self.get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('wallet:money'))
