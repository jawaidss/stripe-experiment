import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from forms import NewCardCheckoutForm, OldCardCheckoutForm
from models import Card, Order
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

    if request.method == 'POST':
        new_card_checkout_form = NewCardCheckoutForm(request.POST)
        old_card_checkout_form = OldCardCheckoutForm(request.POST)

        if new_card_checkout_form.is_valid():
            try:
                stripe_customer = stripe.Customer.create(
                    card=new_card_checkout_form.cleaned_data['stripe_token'],
                    description=user.username,
                    email=user.email
                )
            except stripe.CardError, error:
                messages.error(request, error)
                return HttpResponseRedirect(reverse('shopping-checkout'))
            except stripe.InvalidRequestError:
                messages.error(request, 'Please try again.') # Invalid stripe_token
                return HttpResponseRedirect(reverse('shopping-checkout'))
            else:
                Card.objects.create(user=user, stripe_customer_id=stripe_customer.id)
        elif old_card_checkout_form.is_valid():
            try:
                stripe_customer = stripe.Customer.retrieve(old_card_checkout_form.cleaned_data['stripe_customer_id'])
            except stripe.InvalidRequestError:
                messages.error(request, 'Please try again.') # Invalid stripe_customer_id
                return HttpResponseRedirect(reverse('shopping-checkout'))
            if not user.card_set.filter(stripe_customer_id=stripe_customer.id):
                messages.error(request, 'Please try again.') # Invalid stripe_customer_id
                return HttpResponseRedirect(reverse('shopping-checkout'))
        else:
            messages.error(request, 'Please try again.') # Missing stripe_token and stripe_customer_id
            return HttpResponseRedirect(reverse('shopping-checkout'))

        try:
            stripe_charge = stripe.Charge.create(
                amount=int(cart.total * 100), # in cents
                currency='usd',
                customer=stripe_customer.id,
                description=user.username
            )
        except stripe.CardError, error:
            messages.error(request, error)
            return HttpResponseRedirect(reverse('shopping-checkout'))
        else:
            if stripe_charge.card.cvc_check == 'fail':
                messages.error(request, 'The CVC provided is incorrect.')
                return HttpResponseRedirect(reverse('shopping-checkout'))

            if stripe_charge.card.address_line1_check == 'fail':
                messages.error(request, 'The first address line provided is incorrect.')
                return HttpResponseRedirect(reverse('shopping-checkout'))

            if stripe_charge.card.address_zip_check == 'fail':
                messages.error(request, 'The ZIP code provided is incorrect.')
                return HttpResponseRedirect(reverse('shopping-checkout'))

        order = Order.objects.create(user=user, stripe_charge_id=stripe_charge.id, ip_address=request.META['REMOTE_ADDR'])

        for item in cart.items:
            item.to_model(order).save()

        cart.empty(request)
        messages.success(request, 'You were successfully checked out.')

        send_mail(render_to_string('shopping/receipt_email_subject.txt',
                                   {'user': user, 'order': order}),
                  render_to_string('shopping/receipt_email.txt',
                                   {'site': Site.objects.get_current(), 'order': order}),
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email])

        return HttpResponseRedirect(reverse('shopping-order', args=[order.id]))

    cards = []
    for card in user.card_set.all():
        try:
            cards.append((card, stripe.Customer.retrieve(card.stripe_customer_id)))
        except stripe.InvalidRequestError:
            pass # Invalid stripe_customer_id

    new_card_checkout_form = NewCardCheckoutForm(initial={'name': user.get_full_name()})
    old_card_checkout_form = OldCardCheckoutForm()

    return render_to_response('shopping/checkout.html',
                              {'cart': cart,
                               'new_card_checkout_form': new_card_checkout_form,
                               'old_card_checkout_form': old_card_checkout_form,
                               'cards': cards},
                              RequestContext(request))

@login_required
def orders(request):
    orders = request.user.order_set.all()

    return render_to_response('shopping/orders.html',
                              {'orders': orders},
                              RequestContext(request))

@login_required
def order(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)

    try:
        stripe_charge = stripe.Charge.retrieve(order.stripe_charge_id)
    except stripe.InvalidRequestError:
        stripe_charge = None

    return render_to_response('shopping/order.html',
                              {'order': order,
                               'stripe_charge': stripe_charge},
                              RequestContext(request))