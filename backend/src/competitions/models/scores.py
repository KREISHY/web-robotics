from django.db import models
from .utils import MinMaxFloat
from competitions.models import Competition, Criteria
from users.models import User


class Score(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name="Соревнование",
    )
    judge_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name='Судья',
    )
    criteria = models.ForeignKey(
        Criteria,
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name='Критерий оценки',
    )
    score = MinMaxFloat(
        min_value=0.0,
        max_value=100.0,
        verbose_name='Баллы',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    def __str__(self):
        return f'{self.competition} {self.criteria} {self.score}'

    class Meta:
        verbose_name = 'Балл'
        verbose_name_plural = 'Баллы'
