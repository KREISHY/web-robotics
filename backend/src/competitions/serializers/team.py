from rest_framework import serializers, permissions
from competitions.models import Teams
from competitions.validations.team_register_val import validate_team_register



class TeamSSerializer(serializers.ModelSerializer):
    captain_name = serializers.CharField(source='captain.username', read_only=True)  # Отображение имени капитана
    competition_name = serializers.CharField(source='competition.name', read_only=True)  # Отображение названия соревнования

    class Meta:
        model = Teams
        fields = [
            'name', 'robot_name', 'city', 'institution', 'members',
            'leader', 'captain_name', 'contact_phone', 'comments', 'status',
            'competition_name'
        ]

class TeamRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = [
            'name','robot_name', 'city',
            'institution', 'members', 'leader',
            'contact_phone', 'comments', 'competition'
        ]

        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': 'Пожалуйста, укажите название команды.',
                    'max_length': 'Название команды не может быть длиннее 255 символов.',
                }
            },
            'robot_name': {
                'error_messages': {
                    'blank': 'Пожалуйста, укажите название робота.',
                    'max_length': 'Название робота не может быть длиннее 255 символов.',
                }
            },
            'city': {
                'error_messages': {
                    'blank': 'Пожалуйста, укажите город.',
                    'max_length': 'Название города не может быть длиннее 255 символов.',
                }
            },
            'institution': {
                'error_messages': {
                    'blank': 'Пожалуйста, укажите учебное заведение.',
                    'max_length': 'Название учебного заведения не может быть длиннее 255 символов.',
                }
            },
            'contact_phone': {
                'error_messages': {
                    'blank': 'Пожалуйста, укажите ваш номер телефона.',
                    'invalid': 'Пожалуйста, введите корректный номер телефона.',
                }
            },
            'competition': {
                'error_messages': {
                    'null': 'Пожалуйста, выберите соревнование.',
                }
            },
        }

    def create(self, validated_data):
        # Устанавливаем статус по умолчанию
        validated_data['status'] = 'awaiting'

        # Если не указан лидер, задаем значение по умолчанию
        if not validated_data.get('leader'):
            validated_data['leader'] = "Отсутствует"

        # Присваиваем капитана из текущего пользователя
        user = self.context['request'].user
        validated_data['captain'] = user

        # Создаем объект команды
        return Teams.objects.create(**validated_data)

    def validate(self, data):
        user = self.context['request'].user
        validate_team_register(data, user)
        return data


