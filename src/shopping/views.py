import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import CheckoutForm
from models import Customer
from utils import get_or_create_cart

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def cart(request):
    cart = get_or_create_cart(request)
    return render_to_response('shopping/cart.html',
                              {'cart': cart},
                              RequestContext(request))

@login_required
def empty_cart(request):
    cart = get_or_create_cart(request)

    if cart.is_empty:
        messages.error(request, 'You cannot empty an already empty cart.')
    else:
        cart.empty(request)
        messages.success(request, 'Your cart was successfully emptied.')

    return HttpResponseRedirect(reverse('shopping-cart'))

@login_required
def remove_item_from_cart(request, id):
    cart = get_or_create_cart(request)
    item = cart.remove(request, int(id))

    if item is None:
        messages.error(request, '%s was not removed from your cart.' % id)
    else:
        messages.success(request, '%s was successfully removed from your cart.' % item.name)

    return HttpResponseRedirect(reverse('shopping-cart'))

@login_required
def checkout(request):
    cart = get_or_create_cart(request)

    if cart.is_empty:
        messages.error(request, 'You cannot checkout an empty cart.')
        return HttpResponseRedirect(reverse('shopping-cart'))

    user = request.user

    try:
        customer = user.customer
    except Customer.DoesNotExist:
        customer = None

    if request.method == 'POST':
        if customer is None:
            form = CheckoutForm(request.POST)

            if form.is_valid():
                stripe_customer = stripe.Customer.create(
                    card=form.cleaned_data['stripe_token'],
                    description=user.username,
                    email=user.email
                )
                customer = Customer.objects.create(user=user, stripe_id=stripe_customer.id)
            else:
                messages.error(request, 'Please try again.')
                return HttpResponseRedirect(reverse('shopping-checkout'))

        stripe.Charge.create(
            amount=int(cart.total * 100), # in cents
            currency='usd',
            customer=customer.stripe_id
            # description=...
        )

        order = Order.objects.create(customer=customer)

        for item in cart.items:
            pass
            # Item.objects.create(order=order, ...)

        cart.empty(request)
        messages.success(request, 'You successfully checked out.')
        return HttpResponseRedirect(reverse('main-index'))

    if customer is None:
        form = CheckoutForm(initial={'name': user.get_full_name()})
        card = None
    else:
        form = None
        card = stripe.Customer.retrieve(customer.stripe_id).active_card

    return render_to_response('shopping/checkout.html',
                              {'cart': cart,
                               'form': form,
                               'card': card},
                              RequestContext(request))