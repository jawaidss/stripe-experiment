from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class SimpleSitemap(Sitemap):
    def items(self):
        return (
            'admin:index',
            'auth_login',
            'auth_logout',
            'auth_password_reset',
            'auth_password_reset_complete',
            'auth_password_reset_done',
            'registration_activation_complete',
            'registration_complete',
            'registration_register',
            'main-index',
        )

    def location(self, name):
        return reverse(name)

sitemaps = {
    'simple_sitemap': SimpleSitemap,
}