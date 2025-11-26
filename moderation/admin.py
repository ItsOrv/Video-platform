from django.contrib import admin
from .models import Report, ContentModeration, BannedUser


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported_by', 'report_type', 'content_type', 'content_id', 'status', 'created_at')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('reported_by__username', 'reason', 'review_notes')
    readonly_fields = ('created_at', 'reviewed_at')
    date_hierarchy = 'created_at'
    actions = ['mark_resolved', 'mark_dismissed']
    
    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved', reviewed_by=request.user)
    mark_resolved.short_description = 'Mark selected reports as resolved'
    
    def mark_dismissed(self, request, queryset):
        queryset.update(status='dismissed', reviewed_by=request.user)
    mark_dismissed.short_description = 'Mark selected reports as dismissed'


@admin.register(ContentModeration)
class ContentModerationAdmin(admin.ModelAdmin):
    list_display = ('moderator', 'content_type', 'content_id', 'action', 'created_at')
    list_filter = ('action', 'content_type', 'created_at')
    search_fields = ('moderator__username', 'reason')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(BannedUser)
class BannedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'banned_by', 'is_permanent', 'expires_at', 'banned_at')
    list_filter = ('is_permanent', 'banned_at')
    search_fields = ('user__username', 'reason')
    readonly_fields = ('banned_at',)
    date_hierarchy = 'banned_at'

