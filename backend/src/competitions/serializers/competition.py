from rest_framework import serializers
from competitions.models import Competition, CompetitionTeam


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['name', 'description', 'start_registration', 'end_registration']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'name': {'required': True, 'error_messages': {
                    'required': 'Название соревнования обязательно для заполнения.'
                }
            },
            'description': {'required': False, 'allow_blank': True},
            'start_registration': {
                'required': True, 'error_messages': {
                    'required': 'Дата начала регистрации обязательна.'
                }
            },
            'end_registration': {
                'required': True, 'error_messages': {
                    'required': 'Дата конца регистрации обязательна.'
                }
            },
        }

    def validate(self, data):
        """
        Общая валидация для проверки корректности дат регистрации.
        """
        start_registration = data.get('start_registration')
        end_registration = data.get('end_registration')

        if start_registration and end_registration:
            if end_registration <= start_registration:
                raise serializers.ValidationError({
                    'end_registration': 'Дата конца регистрации должна быть позже даты начала регистрации.'
                })

        return data

    def validate_name(self, value):
        """
        Проверка поля name (например, уникальность).
        """
        if Competition.objects.filter(name=value).exists():
            raise serializers.ValidationError("Соревнование с таким названием уже существует.")
        return value


class CompetitionTeamSerializer(serializers.ModelSerializer):
    # Сериализатор для модели CompetitionTeam
    competition = CompetitionSerializer()  # Вложенный сериализатор для Competition
    team = serializers.StringRelatedField()  # Просто отображаем имя команды (или можно использовать вложенный сериализатор для Teams)

    class Meta:
        model = CompetitionTeam
        fields = ['competition', 'team']
