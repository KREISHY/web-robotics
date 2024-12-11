from django.db import models
from .utils import MinMaxFloat


class Criteria(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название критерия',
    )
    weight = MinMaxFloat(
        min_value=0, max_value=5,
        verbose_name='Вес критерия',
    )

    class Meta:
        verbose_name = "Критерий"
        verbose_name_plural = "Критерии"