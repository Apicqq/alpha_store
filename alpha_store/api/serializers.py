from rest_framework import serializers

from store.models import Product, ShoppingCart, ShoppingCartItem, Category, \
    SubCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField("get_images")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "category",
            "subcategory",
            "images",
        ]

    def get_images(self, obj):
        images = dict()
        for field in ("thumbnail", "medium_image", "large_image"):
            try:
                images[field] = getattr(obj, field).url
            except ValueError:
                images[field] = None
        return images

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ("id", "name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "subcategories",)


class ShoppingCartGetSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField("get_products")
    amount_of_products = serializers.SerializerMethodField(
        "get_amount_of_products")
    total_price = serializers.SerializerMethodField("get_total_price")

    def get_products(self, obj):
        instance = ShoppingCart.objects.get(user=self.context["request"].user)
        return ShoppingCartItemSerializer(
            instance.cart_items.all(),
            context=self.context,
            many=True
        ).data

    def get_amount_of_products(self, obj):
        return obj.cart_items.count()

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in
                   obj.cart_items.all())

    class Meta:
        model = ShoppingCart
        fields = ("products", "amount_of_products", "total_price")


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField(source="product.price")
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = ShoppingCartItem
        fields = ("id", "product", "quantity", "price",)

    def create(self, validated_data):
        product = validated_data.pop("product")
        quantity = validated_data.pop("quantity")
        cart = ShoppingCart.objects.get(user=self.context["request"].user)
        validated_data['cart'] = cart
        try:
            item = cart.cart_items.get(product=product.pk)
            item.quantity += quantity
            item.save()
        except ShoppingCartItem.DoesNotExist:
            item = ShoppingCartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
        return item
