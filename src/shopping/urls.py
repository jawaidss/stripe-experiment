from django.conf.urls import patterns, url

urlpatterns = patterns('shopping.views',
    url(r'^cart/$', 'cart', name='shopping-cart'),
    url(r'^remove-item-from-cart/(?P<id>[\d]+)/$', 'remove_item_from_cart', name='shopping-remove_item_from_cart'),
)