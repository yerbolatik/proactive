from django.db import models

from products.models import Product
from users.models import User


class BasketQueryset(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'basket'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    objects = BasketQueryset().as_manager()

    def __str__(self):
        return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None, False

        if user.is_authenticated:
            baskets = cls.objects.filter(user=user, product=product)
        else:
            session_key = user.session.session_key
            baskets = cls.objects.filter(session_key=session_key, product=product)

        if baskets.exists():
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
        else:
            if user.is_authenticated:
                basket = cls.objects.create(user=user, product=product, quantity=1)
            else:
                session_key = user.session.session_key
                basket = cls.objects.create(session_key=session_key, product=product, quantity=1)

        return basket, True
