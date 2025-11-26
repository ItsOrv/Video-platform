from django.contrib import admin
from .models import Payment, Subscription, VideoPurchase


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'success', 'transaction_id', 'timestamp')
    list_filter = ('status', 'success', 'timestamp', 'payment_method')
    search_fields = ('user__username', 'transaction_id', 'description')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'is_active', 'start_date', 'end_date')
    list_filter = ('subscription_type', 'is_active', 'start_date', 'end_date')
    search_fields = ('user__username',)
    date_hierarchy = 'start_date'


@admin.register(VideoPurchase)
class VideoPurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'purchased_at')
    search_fields = ('user__username', 'video__title')
    date_hierarchy = 'purchased_at'
