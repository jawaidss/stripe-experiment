from django.contrib import admin

from models import Card, Order

class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_customer_id', 'is_default',)
    list_filter = ('is_default',)
    search_fields = ('user__last_name', 'user__first_name', 'user__username', 'stripe_customer_id',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_charge_id', 'ip_address', 'datetime', 'total',)
    search_fields = ('user__last_name', 'user__first_name', 'user__username', 'stripe_charge_id',)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'description', 'price',)
    list_display_links = ('name',)
    search_fields = ('order__user__last_name', 'order__user__first_name', 'order__user__username', 'order__stripe_charge_id', 'name', 'description',)

admin.site.register(Card, CardAdmin)
admin.site.register(Order, OrderAdmin)