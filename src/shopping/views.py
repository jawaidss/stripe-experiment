from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils import get_or_create_cart

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

    # to-do
    cart.empty(request)
    messages.success(request, 'You successfully checked out.')
    return HttpResponseRedirect(reverse('main-index'))