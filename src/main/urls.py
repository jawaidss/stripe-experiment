from django.conf.urls import patterns, url

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='main-index'),
    url(r'^add-item-to-cart/$', 'add_item_to_cart', name='main-add_item_to_cart'),
)