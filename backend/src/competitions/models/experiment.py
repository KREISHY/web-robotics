from django.db import models

from competitions.models import Competition


class Experiment(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
    )

    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        verbose_name="Соревнование",
    )


    class Meta:
        verbose_name = 'Испытание'
        verbose_name_plural = 'Испытания'