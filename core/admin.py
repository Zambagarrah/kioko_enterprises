from django.contrib import admin
from .models import (
    Category,
    Product,
    Order,
    OrderItem,
)

admin.site.register(Category)
admin.site.register(Product)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'payment_method', 'created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'total', 'payment_method', 'created_at')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)