from rest_framework import serializers

from store.models import Product, ShoppingCart


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
        ]  # FIXME

    def get_images(self, obj):
        images = dict()
        for field in ("thumbnail", "medium_image", "large_image"):
            try:
                images[field] = getattr(obj, field).url
            except ValueError:
                images[field] = None
        return images


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"



class ShoppingCartGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ("item", "user",)