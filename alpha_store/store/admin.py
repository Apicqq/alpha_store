from django.contrib import admin

from store.models import Product, Category, SubCategory


class ProductInline(admin.TabularInline):
    """
    Инлайн-класс для отображения продуктов в категориях.
    """

    model = Product
    extra = 1
    readonly_fields = (
        "name",
        "price",
        "category",
        "subcategory",
        "thumbnail",
        "medium_image",
        "large_image",
        "slug",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Базовая админ-панель для модели Product.
    """

    list_display = (
        "name",
        "price",
        "category",
        "subcategory",
        "thumbnail",
    )
    list_display_links = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Базовая админ-панель для модели Category.
    """

    list_display = (
        "name",
        "slug",
        "image",
    )
    inlines = (ProductInline,)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Базовая админ-панель для модели SubCategory.
    """

    list_display = (
        "name",
        "slug",
        "category",
    )
