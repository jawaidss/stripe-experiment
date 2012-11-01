from django.conf.urls import patterns, url

urlpatterns = patterns('shopping.views',
    url(r'^cart/$', 'cart', name='shopping-cart'),
    url(r'^cart/empty/$', 'empty_cart', name='shopping-empty_cart'),
    url(r'^remove-item-from-cart/(?P<id>[\d]+)/$', 'remove_item_from_cart', name='shopping-remove_item_from_cart'),
    url(r'^checkout/$', 'checkout', name='shopping-checkout'),
    url(r'^orders/$', 'orders', name='shopping-orders'),
    url(r'^orders/(?P<id>[\d]+)/$', 'order', name='shopping-order'),
)