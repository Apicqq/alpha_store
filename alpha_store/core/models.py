from django.db import models

from core.constants import NumericalValues as Nv


class BaseNameSlugModel(models.Model):
    name = models.CharField(
        "Название",
        max_length=Nv.NAME_MAX_LENGTH,
    )
    slug = models.SlugField("Слаг", max_length=Nv.NAME_MAX_LENGTH)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[: Nv.NAME_TRUNCATE_VALUE]
