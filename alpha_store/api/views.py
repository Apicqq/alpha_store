from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import ProductSerializer, ProductListSerializer, \
    ShoppingCartGetSerializer, ShoppingCartItemSerializer, CategorySerializer
from store.models import Product, ShoppingCart, ShoppingCartItem, Category
from core.services import _add_to_shopping_cart, _delete_from_shopping_cart, _adjust_quantity


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
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
    def change_quantity(self, request, *args, **kwargs):
        return _adjust_quantity(
            pk=self.get_object().pk,
            request=request,
            serializer_class=ShoppingCartItemSerializer,
            quantity=self.request.data.get("quantity", 1)
        )

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    model = Category
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()

class ShoppingCartViewSet(viewsets.ReadOnlyModelViewSet):
    model = ShoppingCart
    serializer_class = ShoppingCartGetSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ShoppingCart.objects.select_related("user")


    @action(detail=False, methods=("post",), permission_classes=(IsAuthenticated,))
    def clear(self, request):
        for product in ShoppingCartItem.objects.filter(
            cart=request.user.shopping_cart.first()
        ):
            product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
