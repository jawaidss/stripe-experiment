from django.conf.urls import patterns, url

urlpatterns = patterns('shopping.views',
    url(r'^$', 'index', name='shopping-index'),
    url(r'^ajax/add-to-cart/(?P<id>[\d]+)/$', 'ajax_add_to_cart', name='shopping-ajax_add_to_cart'),
    url(r'^ajax/remove-from-cart/(?P<id>[\d]+)/$', 'ajax_remove_from_cart', name='shopping-ajax_remove_from_cart'),
)