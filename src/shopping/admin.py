from django.contrib import admin

from models import Order

class ItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'description', 'price',)
    list_display_links = ('name',)
    search_fields = ('order__user__last_name', 'order__user__first_name', 'order__user__username', 'name', 'description',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'count', 'total',)
    search_fields = ('user__last_name', 'user__first_name', 'user__username',)

admin.site.register(Order, OrderAdmin)