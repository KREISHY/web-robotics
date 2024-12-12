from rest_framework import serializers
from competitions.models import Competition, CompetitionJudges
from users.models import User


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['id', 'name', 'description', 'start_registration', 'end_registration']
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


class CompetitionJudgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionJudges
        fields = ['judge', 'competition']

    def validate(self, data):
        # Проверяем, существует ли судья
        try:
            judge = User.objects.get(id=data['judge'].id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"judge": "Судья не найден."})

        # Проверяем, существует ли соревнование
        try:
            competition = Competition.objects.get(id=data['competition'].id)
        except Competition.DoesNotExist:
            raise serializers.ValidationError({"competition": "Соревнование не найдено."})

        if CompetitionJudges.objects.filter(judge=judge, competition=competition).exists():
            raise serializers.ValidationError({"judge": "Судья уже прикреплён к данному соревнованию"})
        return data
