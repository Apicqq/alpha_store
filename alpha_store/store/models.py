from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Category(models.Model):
    pass


class SubCategory(models.Model):
    pass


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    subcategories = models.ManyToManyField(SubCategory, related_name="products")
    thumbnail = models.ImageField(upload_to="images/thumbnails")
    medium_image = models.ImageField(upload_to="images/medium")
    large_image = models.ImageField(upload_to="images/large")

    def __str__(self):
        return self.name[:30]


class Cart(models.Model):
    pass