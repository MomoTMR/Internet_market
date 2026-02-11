from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at', 'short_text')
    list_filter = ('rating', 'created_at', 'product')
    search_fields = ('user__username', 'product__name', 'text')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def short_text(self, obj):
        """Display first 50 characters of review text."""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Review Text'
