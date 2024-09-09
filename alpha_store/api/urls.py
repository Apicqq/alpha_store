from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet, ShoppingCartViewSet, CategoryViewSet

v1_router = DefaultRouter()

v1_router.register("products", ProductViewSet, "products")
v1_router.register("shopping_cart", ShoppingCartViewSet, "shopping_cart")
v1_router.register("categories", CategoryViewSet, "categories")

urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
