from django.conf.urls import patterns, include, url
from django.contrib import admin

from sitemap import sitemaps

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('main.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^accounts/', include('registration.backends.default.urls')),
)