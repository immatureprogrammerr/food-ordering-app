from django.contrib import admin
from menu.models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'restaurant', 'updated_at')
    search_fields = ('category_name', 'restaurant__restaurant_name')

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = (
            'product_title',
            'category',
            'restaurant',
            'price',
            'is_available',
            'updated_at',
    )
    search_field = (
        'product_title',
        'category__category_name',
        'restaurant__restaurant_name'
    )
    list_filter = ('is_available',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)