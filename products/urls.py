from django.urls import path

from products.views import ProductsListView, ProductDetailsView

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    # ../product/category/<category_id>
    path('category/<int:category_id>/',
         ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product-detail'),
]
