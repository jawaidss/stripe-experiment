from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from shopping.utils import Item, get_or_create_cart

def index(request):
    messages.info(request, 'This is an info message.')
    messages.success(request, 'This is a success message.')
    messages.warning(request, 'This is a warning message.')
    messages.error(request, 'This is an error message.')
    return render_to_response('main/index.html',
                              RequestContext(request))

def _random_item():
    from decimal import Decimal
    from random import shuffle, randint

    WORDS = '''
Eiusmod keytar ullamco, iphone do occupy synth beard street art tumblr wolf keffiyeh bushwick.
Adipisicing raw denim tattooed et hella, food truck incididunt fugiat portland ut blog.
Jean shorts nihil pop-up skateboard selvage.
Kale chips elit sriracha readymade,
dolore pinterest VHS bicycle rights consequat dolor craft beer anim swag consectetur.
Food truck anim cillum duis thundercats,
3 wolf moon pariatur ullamco blog fugiat echo park commodo bushwick umami.
Odio brunch artisan,
portland dolor laboris thundercats odd future authentic occaecat craft beer.
Accusamus art party biodiesel brunch,
aute flexitarian williamsburg irure Austin dolore.
'''.strip().replace('.', '').replace(',', '').replace('\n', ' ').split()

    shuffle(WORDS)

    return Item(
        name=WORDS[-1].title(),
        description=' '.join(WORDS[:10]).capitalize() + '.',
        price=Decimal('%d.%d' % (randint(0, 1000), randint(0, 100)))
    )

@login_required
def add_item_to_cart(request):
    cart = get_or_create_cart(request)
    item = _random_item()
    cart.add(request, item)
    messages.success(request, '%s was successfully added to your cart.' % item.name)
    return HttpResponseRedirect(reverse('shopping-cart'))