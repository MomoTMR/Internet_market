from django.contrib import admin

from reviews.models import Review
from .models import Category, Product


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "image", "is_active")
    list_filter = ("is_active", "category")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ReviewInline]
