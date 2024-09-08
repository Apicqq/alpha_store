from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from api.serializers import ProductSerializer, ProductListSerializer, \
    ShoppingCartGetSerializer
from store.models import Product, ShoppingCart
from core.services import _add_to_shopping_cart


class ProductViewSet(viewsets.ModelViewSet):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related("category", "subcategory")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ProductListSerializer
        return ProductSerializer

    @action(detail=True, methods=("post",))
    def add_to_shopping_cart(self, request, pk):
        return _add_to_shopping_cart(
            pk=pk,
            request=request,
            serializer_class=ShoppingCartGetSerializer
        )

    @add_to_shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request):
        pass


class ShoppingCartViewSet(viewsets.ModelViewSet):
    model = ShoppingCart
    serializer_class = ShoppingCartGetSerializer
    permission_classes = (AllowAny,)
    queryset = ShoppingCart.objects.all()
    pagination_class = None
    http_method_names = ("get",)

