from django.contrib import admin
from .models import (
    Category,
    Product,
    Order,
    OrderItem,
    BankPaymentProof,
    PaymentLog,
)

admin.site.register(Category)
admin.site.register(Product)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('id', 'user__username')

admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')


admin.site.register(OrderItem, OrderItemAdmin)


class BankPaymentProofAdmin(admin.ModelAdmin):
    list_display = ('order', 'uploaded_by', 'verified', 'uploaded_at')
    list_filter = ('verified',)
    search_fields = ('order__id', 'uploaded_by__username')
    actions = ['mark_verified']

    def mark_verified(self, request, queryset):
        queryset.update(verified=True)


admin.site.register(BankPaymentProof, BankPaymentProofAdmin)


class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('order', 'method', 'status', 'reference', 'logged_at')
    list_filter = ('method', 'status')
    search_fields = ('order__id', 'reference')


admin.site.register(PaymentLog, PaymentLogAdmin)
