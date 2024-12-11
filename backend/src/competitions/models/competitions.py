from django.db import models
from .teams import Teams


class Competition(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название соревнования'
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
    start_registration = models.DateTimeField(
        verbose_name='Дата и время начала регистрации',
    )
    end_registration = models.DateTimeField(
        verbose_name='Дата и время конца регистрации',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Соревнование"
        verbose_name_plural = "Соревнования"


class CompetitionTeam(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name='teams',
    )
    team = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
    )