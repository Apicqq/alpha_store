from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import ProductSerializer, ProductListSerializer, \
    ShoppingCartGetSerializer, ShoppingCartItemSerializer
from store.models import Product, ShoppingCart, ShoppingCartItem
from core.services import _add_to_shopping_cart, _delete_from_shopping_cart


class ProductViewSet(viewsets.ModelViewSet):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related("category", "subcategory")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ProductListSerializer
        return ProductSerializer

    @action(detail=True, methods=("post",), permission_classes=(IsAuthenticated,))
    def cart(self, request, *args, **kwargs):
        return _add_to_shopping_cart(
            pk=self.get_object().pk,
            request=request,
            serializer_class=ShoppingCartItemSerializer,
            quantity=self.request.data.get("quantity", 1)
        )

    @cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        return _delete_from_shopping_cart(
            pk=pk,
            request=request,
            model=ShoppingCartItem
        )
    @cart.mapping.patch
    def change_quantity(self, request, pk):
        pass


class ShoppingCartViewSet(viewsets.ModelViewSet):
    model = ShoppingCart
    serializer_class = ShoppingCartGetSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ShoppingCart.objects.all()
    # http_method_names = ("get", "delete",)


    @action(detail=False, methods=("post",), permission_classes=(IsAuthenticated,))
    def clear(self, request):
        for product in ShoppingCartItem.objects.filter(
            cart=request.user.shopping_cart.first()
        ):
            print(product)