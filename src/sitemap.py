from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class SimpleSitemap(Sitemap):
    def items(self):
        return (
            'main-index',
            'admin:index',
        )

    def location(self, name):
        return reverse(name)

sitemaps = {
    'simple_sitemap': SimpleSitemap,
}