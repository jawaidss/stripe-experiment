from django.conf import settings
from django.core.urlresolvers import reverse

def main(request):
    is_active = {
        'index': request.path == reverse('main-index'),
        'cart': request.path == reverse('shopping-cart'),
        'orders': request.path.startswith(reverse('shopping-orders')),
        'change_password': request.path.startswith(reverse('auth_password_change')),
        'log_in': request.path == reverse('auth_login'),
        'sign_up': request.path.startswith(reverse('registration_register')),
    }
    return {
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'IS_ACTIVE': is_active,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'SITE_NAME': settings.SITE_NAME,
    }

def shopping(request):
    return {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }