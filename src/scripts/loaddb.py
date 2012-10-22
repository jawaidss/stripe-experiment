from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

'''
from main.models import Shirt, Fruit
from shopping.models import Customer, Order
'''

def run():
    Site.objects.all().delete()

    site = Site()
    site.id = settings.SITE_ID
    site.name = settings.SITE_NAME
    if settings.DEBUG:
        site.domain = '127.0.0.1:8000'
    else:
        site.domain = 'www.' + settings.SITE_DOMAIN
    site.save()

    for name, email in settings.ADMINS:
        user = User.objects.create_superuser(email.split('@')[0], email, 'temp123')
        user.first_name, user.last_name = name.split()
        user.save()

    '''
    order = Order.objects.create(customer=Customer.objects.create(user=User.objects.get(username='jawaidss'), stripe_id=''))

    Shirt.objects.create(name='Polo', description='Bacon ipsum dolor sit amet ham hock brisket ground round sirloin pork loin corned beef, pastrami ball tip venison pancetta filet mignon capicola tri-tip chuck. Ground round meatloaf prosciutto sausage, strip steak ball tip tenderloin andouille frankfurter pork ham short ribs hamburger bresaola. Hamburger rump filet mignon venison swine pork chop fatback. Capicola drumstick short loin, venison strip steak turkey chicken biltong turducken pork chop prosciutto pork jerky. Bacon sirloin flank, hamburger tri-tip drumstick ham hock pork loin pork chop.', price=49.99, size=Shirt.SMALL, order=order)
    Shirt.objects.create(name='Oxford', description='Boudin beef meatloaf ham hock shank short loin sirloin salami filet mignon hamburger pig biltong spare ribs pork. Short ribs pork chop leberkas cow tail tongue strip steak capicola chuck andouille t-bone. Tenderloin brisket ham hock, strip steak pig tri-tip pastrami beef ham prosciutto turkey filet mignon. Jerky swine beef, frankfurter ribeye prosciutto sirloin sausage cow leberkas andouille chuck tongue ball tip. Shankle turkey boudin ball tip, hamburger rump biltong pork belly flank short ribs bresaola sirloin chicken kielbasa. Swine pancetta pastrami meatball frankfurter, chicken flank. Drumstick beef ribs pork filet mignon.', price=59.99, size=Shirt.SMALL, order=order)
    Shirt.objects.create(name='Graphic T', description='Pork loin kielbasa leberkas tongue ribeye meatball. Pancetta leberkas shoulder boudin shankle tongue. Pastrami shoulder strip steak fatback andouille rump flank pork chop drumstick jerky leberkas shankle. Pork loin cow pork chop ground round frankfurter, ham boudin ribeye turkey beef ribs prosciutto shankle meatball sirloin meatloaf.', price=69.99, size=Shirt.SMALL, order=order)
    Shirt.objects.create(name='Pocket T', description='Swine ball tip frankfurter, pancetta shankle flank spare ribs ribeye capicola cow pork chop fatback kielbasa andouille t-bone. Spare ribs ball tip leberkas, pastrami salami turducken andouille hamburger. Bresaola beef ribs filet mignon, sausage t-bone shoulder venison ribeye pancetta chuck. Andouille kielbasa tenderloin, spare ribs short ribs biltong jerky fatback.', price=100, size=Shirt.MEDIUM, order=order)
    Shirt.objects.create(name='Muscle T', description='Turducken shoulder tail, bresaola kielbasa shank pork tri-tip flank brisket. Prosciutto chicken ground round, short loin brisket corned beef boudin cow. Fatback tail meatball spare ribs chicken. Salami cow strip steak tri-tip shankle shoulder tenderloin drumstick pig sirloin pork chop rump biltong hamburger ball tip.', price=150, size=Shirt.LARGE, order=order)

    Fruit.objects.create(name='Apple', description='Bacon ipsum dolor sit amet ham hock brisket ground round sirloin pork loin corned beef, pastrami ball tip venison pancetta filet mignon capicola tri-tip chuck. Ground round meatloaf prosciutto sausage, strip steak ball tip tenderloin andouille frankfurter pork ham short ribs hamburger bresaola. Hamburger rump filet mignon venison swine pork chop fatback. Capicola drumstick short loin, venison strip steak turkey chicken biltong turducken pork chop prosciutto pork jerky. Bacon sirloin flank, hamburger tri-tip drumstick ham hock pork loin pork chop.', price=1, order=order)
    Fruit.objects.create(name='Banana', description='Boudin beef meatloaf ham hock shank short loin sirloin salami filet mignon hamburger pig biltong spare ribs pork. Short ribs pork chop leberkas cow tail tongue strip steak capicola chuck andouille t-bone. Tenderloin brisket ham hock, strip steak pig tri-tip pastrami beef ham prosciutto turkey filet mignon. Jerky swine beef, frankfurter ribeye prosciutto sirloin sausage cow leberkas andouille chuck tongue ball tip. Shankle turkey boudin ball tip, hamburger rump biltong pork belly flank short ribs bresaola sirloin chicken kielbasa. Swine pancetta pastrami meatball frankfurter, chicken flank. Drumstick beef ribs pork filet mignon.', price=2, order=order)
    Fruit.objects.create(name='Grape', description='Pork loin kielbasa leberkas tongue ribeye meatball. Pancetta leberkas shoulder boudin shankle tongue. Pastrami shoulder strip steak fatback andouille rump flank pork chop drumstick jerky leberkas shankle. Pork loin cow pork chop ground round frankfurter, ham boudin ribeye turkey beef ribs prosciutto shankle meatball sirloin meatloaf.', price=3, order=order)
    Fruit.objects.create(name='Orange', description='Swine ball tip frankfurter, pancetta shankle flank spare ribs ribeye capicola cow pork chop fatback kielbasa andouille t-bone. Spare ribs ball tip leberkas, pastrami salami turducken andouille hamburger. Bresaola beef ribs filet mignon, sausage t-bone shoulder venison ribeye pancetta chuck. Andouille kielbasa tenderloin, spare ribs short ribs biltong jerky fatback.', price=4, order=order)
    Fruit.objects.create(name='Strawberry', description='Turducken shoulder tail, bresaola kielbasa shank pork tri-tip flank brisket. Prosciutto chicken ground round, short loin brisket corned beef boudin cow. Fatback tail meatball spare ribs chicken. Salami cow strip steak tri-tip shankle shoulder tenderloin drumstick pig sirloin pork chop rump biltong hamburger ball tip.', price=5, order=order)
    '''