from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from shopping.utils import get_or_create_cart
from models import Fruit, Shirt

def index(request):
    messages.info(request, 'This is an info message.')
    messages.success(request, 'This is a success message.')
    messages.warning(request, 'This is a warning message.')
    messages.error(request, 'This is an error message.')
    return render_to_response('main/index.html',
                              RequestContext(request))

def _random_item():
    ITEMS = (
        Shirt(name='Polo', description='Bacon ipsum dolor sit amet ham hock brisket ground round sirloin pork loin corned beef, pastrami ball tip venison pancetta filet mignon capicola tri-tip chuck. Ground round meatloaf prosciutto sausage, strip steak ball tip tenderloin andouille frankfurter pork ham short ribs hamburger bresaola. Hamburger rump filet mignon venison swine pork chop fatback. Capicola drumstick short loin, venison strip steak turkey chicken biltong turducken pork chop prosciutto pork jerky. Bacon sirloin flank, hamburger tri-tip drumstick ham hock pork loin pork chop.', price=49.99, size=Shirt.SMALL),
        Shirt(name='Oxford', description='Boudin beef meatloaf ham hock shank short loin sirloin salami filet mignon hamburger pig biltong spare ribs pork. Short ribs pork chop leberkas cow tail tongue strip steak capicola chuck andouille t-bone. Tenderloin brisket ham hock, strip steak pig tri-tip pastrami beef ham prosciutto turkey filet mignon. Jerky swine beef, frankfurter ribeye prosciutto sirloin sausage cow leberkas andouille chuck tongue ball tip. Shankle turkey boudin ball tip, hamburger rump biltong pork belly flank short ribs bresaola sirloin chicken kielbasa. Swine pancetta pastrami meatball frankfurter, chicken flank. Drumstick beef ribs pork filet mignon.', price=59.99, size=Shirt.SMALL),
        Shirt(name='Graphic T', description='Pork loin kielbasa leberkas tongue ribeye meatball. Pancetta leberkas shoulder boudin shankle tongue. Pastrami shoulder strip steak fatback andouille rump flank pork chop drumstick jerky leberkas shankle. Pork loin cow pork chop ground round frankfurter, ham boudin ribeye turkey beef ribs prosciutto shankle meatball sirloin meatloaf.', price=69.99, size=Shirt.SMALL),
        Shirt(name='Pocket T', description='Swine ball tip frankfurter, pancetta shankle flank spare ribs ribeye capicola cow pork chop fatback kielbasa andouille t-bone. Spare ribs ball tip leberkas, pastrami salami turducken andouille hamburger. Bresaola beef ribs filet mignon, sausage t-bone shoulder venison ribeye pancetta chuck. Andouille kielbasa tenderloin, spare ribs short ribs biltong jerky fatback.', price=100, size=Shirt.MEDIUM),
        Shirt(name='Muscle T', description='Turducken shoulder tail, bresaola kielbasa shank pork tri-tip flank brisket. Prosciutto chicken ground round, short loin brisket corned beef boudin cow. Fatback tail meatball spare ribs chicken. Salami cow strip steak tri-tip shankle shoulder tenderloin drumstick pig sirloin pork chop rump biltong hamburger ball tip.', price=150, size=Shirt.LARGE),
        Fruit(name='Apple', description='Bacon ipsum dolor sit amet ham hock brisket ground round sirloin pork loin corned beef, pastrami ball tip venison pancetta filet mignon capicola tri-tip chuck. Ground round meatloaf prosciutto sausage, strip steak ball tip tenderloin andouille frankfurter pork ham short ribs hamburger bresaola. Hamburger rump filet mignon venison swine pork chop fatback. Capicola drumstick short loin, venison strip steak turkey chicken biltong turducken pork chop prosciutto pork jerky. Bacon sirloin flank, hamburger tri-tip drumstick ham hock pork loin pork chop.', price=1),
        Fruit(name='Banana', description='Boudin beef meatloaf ham hock shank short loin sirloin salami filet mignon hamburger pig biltong spare ribs pork. Short ribs pork chop leberkas cow tail tongue strip steak capicola chuck andouille t-bone. Tenderloin brisket ham hock, strip steak pig tri-tip pastrami beef ham prosciutto turkey filet mignon. Jerky swine beef, frankfurter ribeye prosciutto sirloin sausage cow leberkas andouille chuck tongue ball tip. Shankle turkey boudin ball tip, hamburger rump biltong pork belly flank short ribs bresaola sirloin chicken kielbasa. Swine pancetta pastrami meatball frankfurter, chicken flank. Drumstick beef ribs pork filet mignon.', price=2),
        Fruit(name='Grape', description='Pork loin kielbasa leberkas tongue ribeye meatball. Pancetta leberkas shoulder boudin shankle tongue. Pastrami shoulder strip steak fatback andouille rump flank pork chop drumstick jerky leberkas shankle. Pork loin cow pork chop ground round frankfurter, ham boudin ribeye turkey beef ribs prosciutto shankle meatball sirloin meatloaf.', price=3),
        Fruit(name='Orange', description='Swine ball tip frankfurter, pancetta shankle flank spare ribs ribeye capicola cow pork chop fatback kielbasa andouille t-bone. Spare ribs ball tip leberkas, pastrami salami turducken andouille hamburger. Bresaola beef ribs filet mignon, sausage t-bone shoulder venison ribeye pancetta chuck. Andouille kielbasa tenderloin, spare ribs short ribs biltong jerky fatback.', price=4),
        Fruit(name='Strawberry', description='Turducken shoulder tail, bresaola kielbasa shank pork tri-tip flank brisket. Prosciutto chicken ground round, short loin brisket corned beef boudin cow. Fatback tail meatball spare ribs chicken. Salami cow strip steak tri-tip shankle shoulder tenderloin drumstick pig sirloin pork chop rump biltong hamburger ball tip.', price=5),
    )

    from random import choice

    return choice(ITEMS)

@login_required
def add_item_to_cart(request):
    cart = get_or_create_cart(request)
    item = _random_item()
    cart.add(request, item)
    messages.success(request, '%s was successfully added to your cart.' % item.name)
    return HttpResponseRedirect(reverse('shopping-cart'))