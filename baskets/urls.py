from django.urls import path

from baskets import views
from baskets.views import BasketDetailView

app_name = 'baskets'

urlpatterns = [
    path('basket', BasketDetailView.as_view(), name='basket_detail'),

    path('basket_add/', views.basket_add, name='basket_add'),
    path('basket_change/', views.basket_change, name='basket_change'),
    path('basket_remove/', views.basket_remove, name='basket_remove'),
]
