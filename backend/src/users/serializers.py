from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from config import URL_EMAIL_VERIFY, ROOT_URL, URL_USERS_API, URL_PASSWORD_RESET_VERIFY
from users.models import User, EmailVerify, PasswordReset
from users.validations import custom_validate_register, custom_validate_token, custom_validate_reset_request_password, \
    custom_validate_reset_verify_password, custom_validate_user_login


class UserCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'patronymic']


class UserRegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'last_name', 'first_name', 'patronymic', 'password']
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "Укажите ваш email.",
                    "blank": "Пожалуйста, напишите вашу почты.",
                    "invalid": "Пожалуйста, введите корректный адрес почты.",
                }
            },
            "password": {
                "error_messages": {"required": "Введите пароль.", "blank": "Пожалуйста, напишите ваш пароль."}},
            "last_name": {
                "error_messages": {"required": "Введите фамилию.", "blank": "Пожалуйста, напишите вашу фамилию."}},
            "first_name": {
                "error_messages": {"required": "Введите имя.", "blank": "Пожалуйста, напишите ваше имя."}},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            last_name=validated_data.get('last_name', ''),
            first_name=validated_data.get('first_name', ''),
            patronymic=validated_data.get('patronymic', ''),
            is_active=False
        )
        token = EmailVerify.objects.create(user=user)
        EmailMessage(
            'Подтверждение почты', 
            f'URL: {ROOT_URL + URL_USERS_API + URL_EMAIL_VERIFY}{token.url}\n{token.code}',
            to=[user.email]
        ).send()
        return user

    def validate(self, data):
        custom_validate_register(data)
        return data


class EmailTokenCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerify
        fields = ['code', 'url']
        extra_kwargs = {
            "code": {
                "error_messages": {"required": "Пожалуйста, заполните поле кода.", "blank": "Пожалуйста, напишите ваш код."}},
            "url": {
                "error_messages": {"required": "Пожалуйста, заполните поле URL.", "blank": "Пожалуйста, напишите ваш URL."}},
        }

    def create(self, validated_data):
        url = self.context.get('url')
        token = EmailVerify.objects.get(url=url)
        user = token.user
        user.email_confirmed = True
        user.is_active = True
        user.save()
        token.delete()
        return user

    def validate(self, data):
        url = self.context.get('url')
        custom_validate_token(data, url)
        return data


class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = ['email']
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "Пожалуйста, напишите вашу почту.",
                    "blank": "Пожалуйста, напишите вашу почту.",
                    "invalid": "Пожалуйста, введите корректный адрес почты.",
                }
            },
        }

    def create(self, validated_data):
        PasswordReset.objects.filter(email=validated_data['email']).delete()
        reset_token = PasswordReset.objects.create(email=validated_data['email'])
        EmailMessage(
            'Сброс пароля',
            f'URL: {ROOT_URL + URL_USERS_API + URL_PASSWORD_RESET_VERIFY}{reset_token.url}\n{reset_token.code}',
            to=[reset_token.email]
        ).send()
        return reset_token

    def validate(self, data):
        custom_validate_reset_request_password(data)
        return data


class PasswordResetVerifySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, error_messages={
        "required": "Пожалуйста, напишите свой пароль.",
        "blank": "Пожалуйста, напишите свой пароль."
    })

    class Meta:
        model = PasswordReset
        fields = ['code', 'password']
        extra_kwargs = {
            "code": {
                "error_messages": {"required": "Пожалуйста, напишите код.",
                                   "blank": "Пожалуйста, напишите код."}},
        }

    def validate(self, data):
        url = self.context.get('url')
        custom_validate_reset_verify_password(data, url)
        return data

    def create(self, validated_data):
        reset = get_object_or_404(PasswordReset, url=validated_data['url'])
        user = get_object_or_404(User, email=reset.email)
        user.set_password(validated_data['password'])
        user.save()
        reset.delete()
        return user


class UserLoginSerializer(ModelSerializer):
    email = serializers.EmailField(required=True, error_messages={
        "required": "Пожалуйста, напишите вашу почту.",
        "blank": "Пожалуйста, напишите вашу почту.",
        "invalid": "Пожалуйста, введите корректный адрес почты.",
    })

    password = serializers.CharField(write_only=True, required=True, error_messages={
        "required": "Пожалуйста, напишите ваш пароль.",
        "blank": "Пожалуйста, напишите ваш пароль.",
    })

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        custom_validate_user_login(data)
        return data


