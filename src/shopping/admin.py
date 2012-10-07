from django.contrib import admin

from models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price',)
    search_fields = ('name', 'description',)

admin.site.register(Item, ItemAdmin)