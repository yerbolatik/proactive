from django.urls import path

from products.views import ProductsListView, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),

    # ../product/category/<category_id>
    path('category/<int:category_id>/',
         ProductsListView.as_view(), name='category'),

    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),

    # ../products/baskets/add/<product_id>
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/',
         basket_remove, name='basket_remove'),
]
