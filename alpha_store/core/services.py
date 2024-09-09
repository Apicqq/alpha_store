from typing import TypeVar, Type

from django.db.models import Model
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.constants import ErrorMessages as Em
from store.models import User, ShoppingCart, ShoppingCartItem

UserType = TypeVar("UserType", bound=User)
CartType = TypeVar("CartType", bound=ShoppingCart)


def _add_to_shopping_cart(
    pk: int,
    request: Request,
    serializer_class: Type[Serializer],
    quantity: int,
) -> Response:
    """
    Добавление продукта в корзину пользователю.
    :param pk: PK продукта.
    :param request: HTTP-запрос.
    :param serializer_class: Используемый сериализатор.
    :param quantity: Количество добавляемого продукта.
    :return: HTTP-ответ с данными о добавленном продукте и статусом 201.
    """
    shopping_cart = get_or_create_shopping_cart(user=request.user)
    serializer = serializer_class(
        data=dict(cart=shopping_cart.pk, product=pk, quantity=quantity),
        context=dict(request=request),
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def _delete_from_shopping_cart(
    pk: int, request: Request, model: Type[Model]
) -> Response:
    """
    Удаление продукта из корзины пользователя.
    :param pk: PK продукта.
    :param request: HTTP-запрос.
    :param model: Модель для удаления.
    :return: HTTP-ответ со статусом 204 при успешном удалении, 400 — если
    продукт не был найден в корзине.
    """
    if not model.objects.filter(
        cart=request.user.shopping_cart.first(), pk=pk
    ).exists():
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=dict(message=Em.REQUESTED_OBJECT_NOT_FOUND),
        )
    model.objects.filter(cart=request.user.cart.first(), pk=pk).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def get_or_create_shopping_cart(user: UserType) -> CartType:
    """
    Получение либо создание корзины с товарами конкретного пользователя.

    Используется в методах добавления и правки количества продукта в корзине.
    Данный метод введён для уменьшения нагрузки на БД, чтобы не создавать
    корзину каждому существующему пользователю, а создавать её только по
    мере необходимости.

    :param user: Объект пользователя, делающего запрос.
    :return: Объект модели ShoppingCart.
    """
    try:
        shopping_cart = ShoppingCart.objects.get(user=user)
    except ShoppingCart.DoesNotExist:
        shopping_cart = ShoppingCart.objects.create(user=user)
    return shopping_cart


def _adjust_quantity(
    pk: int,
    request: Request,
    serializer_class: Type[Serializer],
    quantity: int,
) -> Response:
    """
    Метод для правки количества продукта в корзине пользователя.

    Метод проверяет, существует ли запрашиваемый объект Продукта в корзине, и
    если нет, то возвращает HTTP-ответ со статусом 400 и соответствущим
    сообщением.
    В случае нахождения товара его количество в корзине изменяется на заданное,
    а также возвращается ответ со статусом 200 и обновленными данными о
    продукте в корзине.
    :param pk: PK продукта.
    :param request: HTTP-запрос.
    :param serializer_class: Класс используемого сериализатора.
    :param quantity: Запрошенное количество продукта для изменения.
    :return: HTTP-ответ со статусом 200 и обновленными данными о продукте, либо
    400 и соответствующим сообщением.
    """
    shopping_cart = get_or_create_shopping_cart(user=request.user)
    try:
        item = shopping_cart.cart_items.get(product=pk)
    except ShoppingCartItem.DoesNotExist:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=dict(message=Em.REQUESTED_OBJECT_NOT_FOUND_IN_CART),
        )

    serializer = serializer_class(
        data=dict(cart=shopping_cart.pk, product=pk, quantity=quantity),
        context=dict(request=request),
        partial=True,
    )
    serializer.is_valid(raise_exception=True)
    serializer.update(instance=item, validated_data=serializer.validated_data)
    return Response(serializer.data, status=status.HTTP_200_OK)
