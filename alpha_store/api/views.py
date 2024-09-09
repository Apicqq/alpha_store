from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import (
    ProductSerializer,
    ProductListSerializer,
    ShoppingCartGetSerializer,
    ShoppingCartItemSerializer,
    CategorySerializer,
    QuantitySerializer,
)
from store.models import Product, ShoppingCart, ShoppingCartItem, Category
from core.services import (
    _add_to_shopping_cart,
    _delete_from_shopping_cart,
    _adjust_quantity,
)


class ProductViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет для модели Product. Предусмотрена пагинация по полю name.

    Помимо GET-запроса, реализованы дополнительные методы при помощи
    декоратора `action`, такие как:
    1. `cart` - POST-запрос, добавление конкретного товара в корзину.
    2. `cart` - DELETE-запрос, удаление конкретного товара из корзины.
    3. `cart` - PATCH-запрос, изменение количества товара в корзине.

    Метод GET может быть использован любым пользователем (в том числе
    неавторизованным). Для доступа к методам, связанным с корзиной,
    пользователю необходимо зарегистрироваться и авторизоваться.
    """

    model = Product
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = Product.objects.select_related("category", "subcategory")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ProductListSerializer
        return ProductSerializer

    @swagger_auto_schema(request_body=QuantitySerializer)
    @action(
        detail=True, methods=("post",), permission_classes=(IsAuthenticated,)
    )
    def cart(self, request, *args, **kwargs):
        """
        Добавить объект продукта в корзину.
        """
        return _add_to_shopping_cart(
            pk=self.get_object().pk,
            request=request,
            serializer_class=ShoppingCartItemSerializer,
            quantity=self.request.data.get("quantity", 1),
        )

    @cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        """
        Удалить объект продукта из корзины.
        """
        return _delete_from_shopping_cart(
            pk=pk, request=request, model=ShoppingCartItem
        )

    @swagger_auto_schema(request_body=QuantitySerializer)
    @cart.mapping.patch
    def change_quantity(self, request, *args, **kwargs):
        """
        Изменить количество товара в корзине.
        """
        return _adjust_quantity(
            pk=self.get_object().pk,
            request=request,
            serializer_class=ShoppingCartItemSerializer,
            quantity=self.request.data.get("quantity", 1),
        )


class CategoryViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет для модели Category. Предусмотрена пагинация по полю name.
    """

    model = Category
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()


class ShoppingCartViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет для модели ShoppingCart.

    Помимо GET-запроса, отображающего состав корзины,
    реализован дополнительный метод `clear` для очистки корзины.
    """

    model = ShoppingCart
    serializer_class = ShoppingCartGetSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ShoppingCart.objects.select_related("user")

    @action(
        detail=False, methods=("post",), permission_classes=(IsAuthenticated,)
    )
    def clear(self, request):
        """
        Очистить корзину с товарами.
        """
        for product in ShoppingCartItem.objects.filter(
            cart=request.user.shopping_cart.first()
        ):
            product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
