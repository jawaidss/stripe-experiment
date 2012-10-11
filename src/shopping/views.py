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
def remove_item_from_cart(request, id):
    cart = get_or_create_cart(request)
    item = cart.remove(request, int(id))

    if item is None:
        messages.error(request, '%s was not removed from your cart.' % id)
    else:
        messages.success(request, '%s was successfully removed from your cart.' % item.name)

    return HttpResponseRedirect(reverse('shopping-cart'))