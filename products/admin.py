from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget

from products.models import Product, ProductCategory, ProductImage

# Register your models here.
admin.site.register(ProductCategory)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Количество дополнительных пустых полей для заполнения


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'short_description', 'description',
              'price', 'quantity', 'category', 'stripe_product_price_id')
    search_fields = ('name',)
    # sort:
    ordering = ('name', )
    inlines = [ProductImageInline]

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
