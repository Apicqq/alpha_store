from django.contrib import admin

from store.models import Product, Category, SubCategory


class ProductInline(admin.TabularInline):
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
    list_display = ("name", "price", "category", "subcategory", "thumbnail",)
    list_display_links = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "image",)
    # list_editable = ("name", "slug",)
    inlines = (ProductInline,)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category",)
    # list_editable = ("name", "slug",)
