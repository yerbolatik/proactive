from django.contrib import admin

from products.models import Basket, Product, ProductCategory

# Register your models here.
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'short_description', 'description',
              'price', 'quantity', 'category', 'stripe_product_price_id')
    search_fields = ('name',)
    # sort:
    ordering = ('name', )


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
