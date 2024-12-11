from django.db import models

from users.models import User


class Log(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    action = models.JSONField(
        null=True, blank=True,
        verbose_name="Изменения"
    )

    timestamp = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время изменения'
    )

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"