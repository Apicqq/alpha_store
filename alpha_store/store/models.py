from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseNameSlugModel

User = get_user_model()

class Product(BaseNameSlugModel):
    thumbnail = models.ImageField(
        "Превью",
        upload_to="images/thumbnails",
        blank=True,
    )
    medium_image = models.ImageField(
        "Изображение среднего размера",
        upload_to="images/medium",
        blank=True,
    )
    large_image = models.ImageField(
        "Изображение большого размера",
        upload_to="images/large",
        blank=True,
    )
    category = models.ForeignKey(
        "Category",
        verbose_name="Категория продукта",
        on_delete=models.CASCADE
    )
    subcategory = models.ForeignKey(
        "SubCategory",
        verbose_name="Подкатегория продукта",
        on_delete=models.CASCADE
    )
    price = models.PositiveSmallIntegerField(
        "Цена продукта",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100000),
        ]
    )

    class Meta:
        default_related_name = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)



class Category(BaseNameSlugModel):
    image = models.ImageField(
        "Изображение",
        upload_to="images/categories",
        blank=True
    )

    class Meta:
        default_related_name = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)



class SubCategory(BaseNameSlugModel):
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE
    )



    class Meta:
        default_related_name = "shopping_cart"
        verbose_name = "Корзина"

    def __str__(self):
        return f"{type(self).__name__} пользователя {self.user}"


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(
        ShoppingCart,
        verbose_name="Корзина с товарами",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product = models.ForeignKey(
        Product,
        related_name="products",
        verbose_name="Продукт",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        "Количество",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ]
    )

    class Meta:
        default_related_name = "shopping_cart_items"
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.product}: {self.quantity}"
