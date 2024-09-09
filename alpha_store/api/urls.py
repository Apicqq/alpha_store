from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet, ShoppingCartViewSet, CategoryViewSet

v1_router = DefaultRouter()

v1_router.register("products", ProductViewSet, "products")
v1_router.register("shopping_cart", ShoppingCartViewSet, "shopping_cart")
v1_router.register("categories", CategoryViewSet, "categories")


schema_view = get_schema_view(
    openapi.Info(
        title="API документация для проекта Интернет-магазин",
        default_version="v1",
        description="Здесь описаны API для работы с интернет-магазином.",
        contact=openapi.Contact(email="apic@yandex.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
