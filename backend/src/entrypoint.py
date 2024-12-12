import os
import django

# Установка переменной окружения для конфигурации Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Инициализация приложений Django
django.setup()

from django.contrib.auth.models import Group
from users.models import User
from config import SUPERUSER_EMAIL, SUPERUSER_PASSWORD

try:
    if not User.objects.filter(email=SUPERUSER_EMAIL).exists():
        User.objects.create_superuser(
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD,
            username='admin',
            first_name='Admin',
            last_name='Admin',
            patronymic='Admin',
            email_confirmed=True,
        )
        print(f"Суперпользователь успешно создан.")
    else:
        print(f"Суперпользователь уже существует.")
except Exception as e:
    print(f"Ошибка при создании суперпользователя: {e}")

try:
    # Проверка и создание группы "Administrator"
    admin_group, created = Group.objects.get_or_create(name='Operators')
    if created:
        print("Группа 'Operators' была создана.")
    else:
        print("Группа 'Operators' уже существует.")

    # Проверка и создание группы "Judges"
    judges_group, created = Group.objects.get_or_create(name='Judges')
    if created:
        print("Группа 'Judges' была создана.")
    else:
        print("Группа 'Judges' уже существует.")

except Exception as e:
    print(f"Ошибка при создании групп: {e}")