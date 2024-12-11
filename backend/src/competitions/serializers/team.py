from rest_framework import serializers
from competitions.models import Teams, TeamMembers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User (если требуется информация о пользователе)."""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic', ]


class TeamsSerializer(serializers.ModelSerializer):
    leader = UserSerializer()  # Вложенный сериализатор для руководителя команды
    members = serializers.CharField()  # Преобразуем текстовое поле в строку
    status_display = serializers.CharField(source='get_status_display')  # Отображаем статус в человекочитаемом виде

    class Meta:
        model = Teams
        fields = [
            'name', 'robot_name', 'city', 'institution',
            'members', 'leader', 'contact_phone', 'contact_email',
            'comments', 'status', 'status_display'
        ]


class TeamMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Вложенный сериализатор для пользователя
    team = TeamsSerializer()  # Вложенный сериализатор для команды

    class Meta:
        model = TeamMembers
        fields = ['user', 'team']
