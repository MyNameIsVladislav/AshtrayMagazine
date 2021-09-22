from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from orderapp.models import OrderItem
from orderapp.forms import OrderCreateForm
from cart.cart import Cart
from core.settings import EMAIL_HOST_USER
from purse.models import PurseModel
from shopapp.models import Product


def send_email_success(cart, user, email):
    msg_html = render_to_string('order/email.html', {'cart': cart, 'user': user})
    send_mail('Successful', msg_html, EMAIL_HOST_USER, [email], html_message=msg_html)


def not_product(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    return render(request, 'order/not_product.html', {'product': product})


def not_money(request):
    return render(request, 'order/not_money.html')


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            return pay_product(request, order, cart)
    user_info = {
        'user': request.user,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    form = OrderCreateForm(initial=user_info)

    return render(request, 'order/order_create.html',
                  {'cart': cart, 'form': form})


@transaction.atomic
def pay_product(request, order, cart):
    try:
        user_wallet = PurseModel.objects.filter(user_id=request.user).first()
        user_wallet.money -= order.get_total_cost()
        user_wallet.save()
    except IntegrityError:
        return HttpResponseRedirect(reverse('order:not_money'))
    for item in order.items.all():
        try:
            item.product.stock -= item.quantity
            item.product.save()
        except IntegrityError:
            return HttpResponseRedirect("%s?del=prod" % reverse('cart:cart_remove', args=(item.product.pk,)))

    send_email_success(cart, request.user, order.email)
    cart.clear()
    return render(request, 'order/order_created.html')
