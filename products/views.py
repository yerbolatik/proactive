from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Product, ProductCategory
from baskets.models import Basket
from informations.models import DeliveryInformation, ReturnInformation


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Proactive'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['title'] = 'Proactive - Каталог'
        context['categories'] = ProductCategory.objects.all()
        context['current_category'] = ProductCategory.objects.get(
            id=self.kwargs.get('category_id')) if self.kwargs.get('category_id') else None
        return context


class ProductDetailsView(TitleMixin, DetailView):
    model = Product
    template_name = 'products/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        similar_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)
        context['similar_products'] = similar_products
        # Получаем список изображений для текущего продукта
        product_images = product.images.all()
        context['product_images'] = product_images
        context['product_name'] = product.name

        delivery_info_long = get_object_or_404(DeliveryInformation, name='long')
        context['delivery_info_long'] = delivery_info_long
        return_info = get_object_or_404(ReturnInformation, name='return')
        context['return_info'] = return_info

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        # quantity = form.cleaned_data['quantity']
        quantity = int(form.data['quantity'])
        baskets = Basket.objects.filter(user=self.request.user, product=product)

        if not baskets.exists():
            Basket.objects.create(user=self.request.user, product=product, quantity=quantity)
        else:
            basket = baskets.first()
            basket.quantity += quantity
            basket.save()

        return redirect('baskets:basket_detail')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
