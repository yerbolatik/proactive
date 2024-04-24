from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token

from orders.views import stripe_webhook_view
from products.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    # site adress, def index in views.py,
    # name='index' - для того, чтобы в html-файле использовать это имя

    path('products/', include('products.urls', namespace='products')),
    # include - позволяет подключать маршруты из других файлов urls.py в основной файл маршрутизации.
    # namespace - указывает пространство имен для URL этого приложения.

    path('users/', include('users.urls', namespace='users')),
    path('basket/', include('baskets.urls', namespace='basket')),
    path('accounts/', include('allauth.urls')),
    path('orders/', include('orders.urls', namespace='orders')),

    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook'),

    path('api/', include('api.urls', namespace='api')),
    path('api-token-auth/', obtain_auth_token)

]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
