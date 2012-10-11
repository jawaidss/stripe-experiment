from django.contrib import admin

from shopping.admin import ItemAdmin
from models import Shirt, Fruit

class ShirtAdmin(ItemAdmin):
    list_display = ItemAdmin.list_display + ('size',)
    search_fields = ItemAdmin.search_fields + ('size',)

class FruitAdmin(ItemAdmin):
    pass

admin.site.register(Shirt, ShirtAdmin)
admin.site.register(Fruit, FruitAdmin)