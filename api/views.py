from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from baskets.models import Basket
from products.models import Product
from products.serializers import BasketSerializer, ProductSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()


class BasketsModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(BasketsModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('product_id')
            if not product_id:
                return Response({'product_id': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            user = self.request.user
            basket_qs = Basket.objects.filter(product_id=product_id, user=user)
            if basket_qs.exists():
                basket_instance = basket_qs.first()
                serializer = self.get_serializer(basket_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                obj, is_created = Basket.create_or_update(product_id, user)
                status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
                serializer = self.get_serializer(obj)
                return Response(serializer.data, status=status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
