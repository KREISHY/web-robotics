from django.db import models

from users.models import User


class Teams(models.Model):
    STATUS_CHOICES = [
        ('аwaiting', 'Ожидание подтверждения'),
        ('rejected', 'Отклонено'),
        ('approved', 'Подтверждены'),
        ('registered', 'Зарегистрированы'),
        ('disqualification', 'Дисквалификация')
    ]

    name = models.CharField(
        max_length=255,
        verbose_name="Название команды",
    )

    robot_name = models.CharField(
        max_length=255,
        verbose_name="Название робота"
    )

    city = models.CharField(
        max_length=255,
        verbose_name="Город"
    )

    institution = models.CharField(
        max_length=255,
        verbose_name="Учебное заведение"
    )

    members = models.TextField(
        blank=True,
        null=True,
        verbose_name='Члены команды',
    )
    leader = models.CharField(
        verbose_name='Руководитель команды',
        max_length=255,
        blank=True,
        help_text='Обычно преподаватель'
    )

    captain = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Капитан команды'
    )

    contact_phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )

    comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="Комментарий"
    )

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус команды"
    )

    competition = models.ForeignKey(
        'competitions.Competition',  # Строковая ссылка
        on_delete=models.CASCADE,
        related_name='teams',
        verbose_name='Соревнование'
    )

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"