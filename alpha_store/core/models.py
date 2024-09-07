from django.db import models


class BaseNameSlugModel(models.Model):
    name = models.CharField(
        "Название",
        max_length=255,
    )
    slug = models.SlugField(
        "Слаг",
        max_length=255
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:30]
