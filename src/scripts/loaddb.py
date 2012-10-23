from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

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