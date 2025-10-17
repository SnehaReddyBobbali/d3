from django.contrib import admin
from .models import LostItem, Claim


@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'location_lost', 'date_lost', 'posted_by', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'location_lost']
    date_hierarchy = 'created_at'


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['item', 'claimed_by', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['item__title', 'claimed_by__email', 'message']
    date_hierarchy = 'created_at'
