from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string

from orderapp.models import OrderItem
from orderapp.forms import OrderCreateForm
from cart.cart import Cart
from core.settings import EMAIL_HOST_USER


@login_required
def order_create(request):
    cart = Cart(request)
    print(cart)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            msg_html = render_to_string('order/email.html', {'cart': cart, 'user': request.user})

            send_mail('Successful', msg_html, EMAIL_HOST_USER, [order.email], html_message=msg_html)
            order.save()

            for item in cart:
                OrderItem.objects.create(
                                         order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                        )

            # очистка корзины
            cart.clear()
            return render(request, 'order/order_created.html',
                          )
    else:
        user_info = {
            'user': request.user,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = OrderCreateForm(initial=user_info)

    return render(request, 'order/order_create.html',
                  {'cart': cart, 'form': form})
