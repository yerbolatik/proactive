import stripe
from django.conf import settings
from django.db import models


from users.models import User

# Create your models here.
stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    # строка с max 128 символов
    name = models.CharField(max_length=128, unique=True)
    # большой текст / может быть пустым
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    short_description = models.TextField(max_length=256, default='Описание')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    discount = models.DecimalField(default=0, max_digits=6, decimal_places=0, verbose_name="%")
    quantity = models.PositiveIntegerField(default=0)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Продукт: {self.name} | Категория: {self.category}"

    def sell_price(self):
        if self.discount:
            return (self.price - self.price*self.discount/100)
        else:
            return self.price

    def save(self, *args, **kwargs):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super().save(*args, **kwargs)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='kzt')
        return stripe_product_price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images')
