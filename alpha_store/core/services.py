from typing import TypeVar, Type

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from store.models import User, ShoppingCart, ShoppingCartItem

UserType = TypeVar("UserType", bound=User)
CartType = TypeVar("CartType", bound=ShoppingCart)


def _add_to_shopping_cart(pk: int, request: Request, serializer_class: Type[Serializer],
                          quantity, partial: bool = False) -> Response:
    shopping_cart = get_or_create_shopping_cart(user=request.user)
    serializer = serializer_class(
        data=dict(
            cart=shopping_cart.pk,
            product=pk,
            quantity=quantity
        ),
        context=dict(request=request),
        partial=partial
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def _delete_from_shopping_cart(pk: int, request: Request, model) -> Response:
    if not model.objects.filter(
            cart=request.user.shopping_cart.first(),
            pk=pk
    ).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=dict(
                            message="Запрашиваемый объект не найден"
                        ))
    model.objects.filter(
        cart=request.user.cart.first(),
        pk=pk
    ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def get_or_create_shopping_cart(user: UserType) -> CartType:
    try:
        shopping_cart = ShoppingCart.objects.get(user=user)
    except ShoppingCart.DoesNotExist:
        shopping_cart = ShoppingCart.objects.create(user=user)
    return shopping_cart


def _adjust_quantity(pk: int, request: Request, serializer_class, quantity) -> Response:
    shopping_cart = get_or_create_shopping_cart(user=request.user)
    try:
        item = shopping_cart.cart_items.get(product=pk)
    except ShoppingCartItem.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=dict(
                            message="Запрашиваемый объект не найден в вашей корзине"
                        ))

    serializer = serializer_class(
        data=dict(
            cart=shopping_cart.pk,
            product=pk,
            quantity=quantity
        ),
        context=dict(request=request),
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.update(instance=item, validated_data=serializer.validated_data)
    return Response(serializer.data, status=status.HTTP_200_OK)