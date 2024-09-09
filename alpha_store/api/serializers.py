from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from store.models import (
    Product,
    ShoppingCart,
    ShoppingCartItem,
    Category,
    SubCategory,
)


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    """

    class Meta:
        model = Product
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Дополнительно реализовано поле images, содержащее ссылки на изображения
    продуктов в трёх форматах.
    """

    images = serializers.SerializerMethodField("get_images")

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "price",
            "category",
            "subcategory",
            "images",
        )

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_images(self, obj) -> dict[str, str | None]:
        images = dict()
        for field in ("thumbnail", "medium_image", "large_image"):
            try:
                images[field] = getattr(obj, field).url
            except ValueError:
                images[field] = None
        return images


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SubCategory.
    """

    class Meta:
        model = SubCategory
        fields = ("id", "name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Дополнительно реализовано поле subcategories, которое содержит в себе
    вложенный сериализатор SubCategorySerializer, представляющий собой
    связанные подкатегории.
    """

    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "image",
            "subcategories",
        )


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продукта, находящегося в продуктовой корзине.

    Дополнительно реализовано поле price (это поле подтягивает стоимость
    продукта в корзине), а также product (подтягивает продукт из соответствующей
    модели).
    """

    price = serializers.ReadOnlyField(source="product.price")
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = ShoppingCartItem
        fields = (
            "id",
            "product",
            "quantity",
            "price",
        )

    def create(self, validated_data):
        product = validated_data.pop("product")
        quantity = validated_data.pop("quantity")
        cart = ShoppingCart.objects.get(user=self.context["request"].user)
        validated_data["cart"] = cart
        try:
            item = cart.cart_items.get(product=product.pk)
            item.quantity += quantity
            item.save()
        except ShoppingCartItem.DoesNotExist:
            item = ShoppingCartItem.objects.create(
                cart=cart, product=product, quantity=quantity
            )
        return item


class ShoppingCartGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ShoppingCart.

    Реализованы такие дополнительне поля, как products (отвечаает за вывод
    списка продуктов в корзине), amount_of_products (отображает общее
    количество продуктов в корзине пользователя), и total_price (это поле
    рассчитывает стоимость всех продуктов в корзине, учитывая их количество).
    """

    products = serializers.SerializerMethodField("get_products")
    amount_of_products = serializers.SerializerMethodField(
        "get_amount_of_products"
    )
    total_price = serializers.SerializerMethodField("get_total_price")

    @swagger_serializer_method(serializer_or_field=ShoppingCartItemSerializer)
    def get_products(self, obj):
        instance = ShoppingCart.objects.get(user=self.context["request"].user)
        return ShoppingCartItemSerializer(
            instance.cart_items.all(), context=self.context, many=True
        ).data

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_amount_of_products(self, obj) -> int:
        return obj.cart_items.count()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_total_price(self, obj) -> int:
        return sum(
            item.product.price * item.quantity for item in obj.cart_items.all()
        )

    class Meta:
        model = ShoppingCart
        fields = ("products", "amount_of_products", "total_price")
