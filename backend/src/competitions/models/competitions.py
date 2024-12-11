from django.db import models
from .teams import Teams


class Competition(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название соревнования'
    )
    team = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        verbose_name='Команда',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание соревнования',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Соревнование"
        verbose_name_plural = "Соревнования"