from rest_framework import serializers
from users.models import User
from users.validations import custom_validate_register


class UserCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'patronymic', 'password']


class UserRegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'last_name', 'first_name', 'patronymic', 'password']
        extra_kwargs = {
            "email": {
                "error_messages": {"required": "Укажите ваш email.", "blank": "Пожалуйста, заполните поле почты."}},
            "password": {
                "error_messages": {"required": "Введите пароль.", "blank": "Пожалуйста, заполните поле пароля."}},
            "last_name": {
                "error_messages": {"required": "Введите фамилию.", "blank": "Пожалуйста, заполните поле фамилии."}},
            "first_name": {
                "error_messages": {"required": "Введите имя.", "blank": "Пожалуйста, заполните поле имени."}},
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
        return user


    def validate(self, data):
        custom_validate_register(data)
        return data


