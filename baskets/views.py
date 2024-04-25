from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView

from baskets.models import Basket
from baskets.utils import get_user_baskets
from common.views import TitleMixin
from informations.models import DeliveryInformation
from products.models import Product


class BasketDetailView(TitleMixin, TemplateView):
    template_name = 'baskets/basket.html'
    title = 'Корзина'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        context['baskets'] = baskets
        delivery_info_short = get_object_or_404(DeliveryInformation, name='short')
        context['delivery_info_short'] = delivery_info_short
        return context


def basket_add(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user, product=product)
        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets = Basket.objects.filter(
            session_key=request.session.session_key, product=product)

        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(
                session_key=request.session.session_key, product=product, quantity=1)

    user_basket = get_user_baskets(request)
    basket_items_html = render_to_string(
        "baskets/basket.html", {"baskets": user_basket}, request=request)

    delivery_info_short = DeliveryInformation.objects.get(name="short")

    response_data = {
        "message": "Товар добавлен в корзину",
        "basket_items_html": basket_items_html,
        "delivery_info_html": delivery_info_short.text,
    }

    return JsonResponse(response_data)


def basket_change(request):
    basket_id = request.POST.get("basket_id")
    quantity = request.POST.get("quantity")

    basket = Basket.objects.get(id=basket_id)

    basket.quantity = quantity
    basket.save()

    updated_quantity = basket.quantity

    basket = get_user_baskets(request)
    basket_items_html = render_to_string(
        "baskets/basket.html", {"baskets": basket}, request=request)

    delivery_info_short = DeliveryInformation.objects.get(name="short")

    response_data = {
        "basket_items_html": basket_items_html,
        "quantity": updated_quantity,
        "delivery_info_html": delivery_info_short.text,
    }

    return JsonResponse(response_data)


def basket_remove(request):

    basket_id = request.POST.get("basket_id")

    basket = Basket.objects.get(id=basket_id)
    quantity = basket.quantity
    basket.delete()

    user_basket = get_user_baskets(request)
    basket_items_html = render_to_string(
        "baskets/basket.html", {"baskets": user_basket}, request=request)

    delivery_info_short = DeliveryInformation.objects.get(name="short")

    response_data = {
        "message": "Товар удален",
        "basket_items_html": basket_items_html,
        "quantity_deleted": quantity,
        "delivery_info_html": delivery_info_short.text,
    }

    return JsonResponse(response_data)
