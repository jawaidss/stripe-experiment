from django.contrib import admin

from models import Customer, Order

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_id',)
    search_fields = ('user__last_name', 'user__first_name', 'user__username', 'stripe_id',)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'description', 'price',)
    list_display_links = ('name',)
    search_fields = ('order__customer__user__last_name', 'order__customer__user__first_name', 'order__customer__user__username', 'order__customer__stripe_id', 'name', 'description',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'datetime', 'total',)
    search_fields = ('customer__user__last_name', 'customer__user__first_name', 'customer__user__username', 'customer__stripe_id',)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)