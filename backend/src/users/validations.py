import re

from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from users.models import User, EmailVerify, PasswordReset

# Валидаторы
def custom_validate_email(email):
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError({'email': 'Эта почта уже используется.'})

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise serializers.ValidationError({'email': 'Введите корректный адрес электронной почты.'})

    forbidden_domains = ['tempmail.com', 'example.com']
    domain = email.split('@')[1]
    if domain in forbidden_domains:
        raise serializers.ValidationError({'email': 'Использование этих почтовых сервисов запрещено.'})
    return email

def custom_validate_password(password):
    # TODO: Добавить валидацию перед продом
    return password

def custom_validate_first_name(first_name):
    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]+$", first_name):
        raise serializers.ValidationError({'first_name': 'Имя должно содержать только буквы.'})
    return first_name

def custom_validate_last_name(last_name):
    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]+$", last_name):
        raise serializers.ValidationError({'last_name': 'Фамилия должна содержать только буквы.'})
    return last_name

def custom_validate_patronymic(patronymic):
    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]+$", patronymic):
        raise serializers.ValidationError({'patronymic': 'Отчество должно содержать только буквы.'})
    return patronymic

def custom_validate_username(username):
    # Проверка, что username содержит только допустимые символы
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        raise serializers.ValidationError({'username': 'Имя пользователя может содержать только буквы, цифры и символы "_".'})

    # Проверка уникальности username
    if User.objects.filter(username=username).exists():
        raise serializers.ValidationError({'username': 'Это имя пользователя уже занято. Пожалуйста, выберите другое.'})


# Валидация регистрации
def custom_validate_register(data):
    email = data.get('email')
    if not email:
        raise serializers.ValidationError({'email': 'Пожалуйста, введите вашу почту.'})
    custom_validate_email(email)

    password = data.get('password')
    if not password:
        raise serializers.ValidationError({'password': 'Пожалуйста, заполните ваш пароля.'})
    custom_validate_password(password)

    last_name = data.get('last_name')
    if not last_name:
        raise serializers.ValidationError({'last_name': 'Пожалуйста, заполните вашу фамилии.'})
    custom_validate_last_name(last_name)

    first_name = data.get('first_name')
    if not first_name:
        raise serializers.ValidationError({'first_name': 'Пожалуйста, заполните ваше имени.'})
    custom_validate_first_name(first_name)

    patronymic = data.get('patronymic')
    if patronymic:
        custom_validate_patronymic(patronymic)

    username = data.get('username')
    custom_validate_username(username)

# Валидация токенов
def custom_validate_token(data, url):
    custom_validate_email_token_url(url)
    custom_validate_email_token_code(data, url)

def custom_validate_email_token_url(url):
    if not url:
        raise serializers.ValidationError({'url': 'Пожалуйста, укажите URL подтверждения.'})
    if not EmailVerify.objects.filter(url=url).exists():
        raise serializers.ValidationError({'url': 'Неверный URL подтверждения.'})

def custom_validate_email_token_code(data, url):
    code = data.get('code')
    if code is None:
        raise serializers.ValidationError({'code': "Пожалуйста, введите ваш код."})
    if not isinstance(code, int):
        raise serializers.ValidationError({'code': "Код должен быть числом."})
    if not (100000 <= code <= 999999):
        raise serializers.ValidationError({'code': "Код должен быть шестизначным."})

    token = EmailVerify.objects.filter(code=code, url=url).first()
    if not token:
        raise serializers.ValidationError({'code': "Неверный код подтверждения."})

    if token.is_expired():
        token.user.delete()
        token.delete()
        raise serializers.ValidationError({'code': "Истекло время за которое можно поменять пароль."})

    if token.user.is_active:
        raise serializers.ValidationError({'code': "Почта уже подтверждена."})

# Валидация запроса сброса пароля
def custom_validate_reset_request_password(data):
    email = data.get("email")
    if not email:
        raise serializers.ValidationError({'email': 'Пожалуйста, укажите почту.'})

    user = User.objects.filter(email=email).first()
    if not user:
        raise serializers.ValidationError({'email': 'Пользователя с данной почтой не существует.'})
    if not user.is_active and not user.email_confirmed:
        raise serializers.ValidationError({'email': 'Подтвердите почту, чтобы затем сменить пароль.'})


# Валидация сброса пароля
def custom_validate_reset_verify_password(data, url):
    if not url:
        raise serializers.ValidationError({'url': 'Пожалуйста, укажите URL для сброса пароля.'})
    if not PasswordReset.objects.filter(url=url).exists():
        raise serializers.ValidationError({'url': 'Неверный URL для сброса пароля.'})
    data['url'] = url

    code = data.get('code')
    if code is None:
        raise serializers.ValidationError({'code': 'Код подтверждения обязателен.'})
    if not isinstance(code, int):
        raise serializers.ValidationError({'code': 'Код подтверждения должен быть числом.'})
    if not (100000 <= code <= 999999):
        raise serializers.ValidationError({'code': 'Код должен быть шестизначным.'})
    if not PasswordReset.objects.filter(code=code, url=url).exists():
        raise serializers.ValidationError({'code': 'Неверный код подтверждения для почты.'})

    reset = PasswordReset.objects.filter(code=code, url=url).first()
    if reset.is_expired():
        reset.delete()
        raise serializers.ValidationError({'code': "Токен сброса пароля истек."})

    password = data.get('password')
    if not password:
        raise serializers.ValidationError({'password': 'Пожалуйста, заполните поле пароля.'})

    custom_validate_password(password)

def custom_validate_username_login(username):
    if not User.objects.filter(username=username).exists():
        raise serializers.ValidationError({'username': 'Данное имя пользователя не существует.'})

def custom_validate_password_login(data):
    password = data.get('password')
    email = data.get('email')

    if not password:
        raise serializers.ValidationError({"password": "Пожалуйста, введите ваш пароль."})

    user = User.objects.filter(email=email).first()
    if user and not check_password(password, user.password):
        raise serializers.ValidationError({"password": "Неверный пароль."})

def custom_validate_user_login(data):
    custom_validate_password_login(data)

    if data.get('email'):
        custom_validate_email_login(data)

    if data.get('username'):
        custom_validate_username_login(data.get('username'))

def custom_validate_email_login(data):
    email = data.get('email')
    if not email:
        raise serializers.ValidationError({"email": "Пожалуйста, введите вашу почту."})

    user = User.objects.filter(email=email).first()
    if not user:
        raise serializers.ValidationError({"email": "Пользователь с такой почтой не найден."})


def validate_judge_register(data):
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    patronymic = data.get('patronymic')

    if email:
        custom_validate_email(email)

    if password:
        custom_validate_password(password)

    custom_validate_first_name(first_name)
    custom_validate_last_name(last_name)

    if patronymic:
        custom_validate_patronymic(patronymic)

