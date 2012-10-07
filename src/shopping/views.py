from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from models import Item

class Cart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add(self, item):
        if item not in self.items:
            self.items.append(item)
            self.items.sort(key=lambda item: item.name)
            self.total += item.price
            return True

        return False

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            self.total -= item.price
            return True

        return False

@login_required
def index(request):
    items = Item.objects.all()
    cart = request.session.get('shopping-cart', Cart())
    return render_to_response('shopping/index.html',
                              {'items': items,
                               'cart': cart},
                              RequestContext(request))

def ajax_add_to_cart(request, id):
    if not request.is_ajax():
        return HttpResponseRedirect(reverse('shopping-index'))

    if request.user.is_anonymous():
        return HttpResponse(simplejson.dumps({'error': 'You are not logged in.'}))

    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return HttpResponse(simplejson.dumps({'error': '%s is an invalid item id.' % id}))

    cart = request.session.setdefault('shopping-cart', Cart())
    if cart.add(item):
        request.session.modified = True
        return HttpResponse(simplejson.dumps({
            'item': {
                'name': item.name,
                'price': str(item.price),
                'ajax_remove_from_cart_url': reverse('shopping-ajax_remove_from_cart',
                                                     args=[item.id])
            },
            'total': str(cart.total),
            'success': '%s was added to your cart.' % item.name
        }))

    return HttpResponse(simplejson.dumps({'error': '%s is already in your cart.' % item.name}))

def ajax_remove_from_cart(request, id):
    if not request.is_ajax():
        return HttpResponseRedirect(reverse('shopping-index'))

    if request.user.is_anonymous():
        return HttpResponse(simplejson.dumps({'error': 'You are not logged in.'}))

    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return HttpResponse(simplejson.dumps({'error': '%s is an invalid item id.' % id}))

    cart = request.session.get('shopping-cart', Cart())
    if cart.remove(item):
        request.session.modified = True
        return HttpResponse(simplejson.dumps({
            'id': item.id,
            'total': str(cart.total),
            'success': '%s was removed from your cart.' % item.name
        }))

    return HttpResponse(simplejson.dumps({'error': '%s is not in your cart.' % item.name}))