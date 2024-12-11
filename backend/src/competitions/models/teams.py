from django.db import models

from users.models import User


class Teams(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('approved', 'Approved'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название команды")
    robot_name = models.CharField(max_length=255, verbose_name="Название робота")
    city = models.CharField(max_length=255, verbose_name="Город")
    institution = models.CharField(max_length=255, verbose_name="Учебное заведение")
    members = models.TextField(
        blank=True,
        null=True,
        verbose_name='Члены команды',
    )
    leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Руководитель команды',
    )
    contact_phone = models.CharField(max_length=20, verbose_name="Телефон")
    contact_email = models.EmailField(verbose_name="Почта")
    comments = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус команды"
    )

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"


class TeamMembers(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    team = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
    )