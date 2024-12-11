from rest_framework import serializers
from competitions.models import Score
from competitions.models import Competition, Criteria
from users.models import User
from competitions.models import Teams  # Импортируем модель Teams


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User (если требуется информация о пользователе)."""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CompetitionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Competition."""
    class Meta:
        model = Competition
        fields = ['name', 'description', 'created_at', 'updated_at']


class CriteriaSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Criteria."""
    class Meta:
        model = Criteria
        fields = ['id', 'name', 'weight']


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Teams."""
    class Meta:
        model = Teams
        fields = ['name', 'robot_name', 'city', 'institution', 'status']


class ScoreSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer()  # Вложенный сериализатор для соревнования
    judge_user = UserSerializer()  # Вложенный сериализатор для судьи
    criteria = CriteriaSerializer()  # Вложенный сериализатор для критерия
    team = TeamSerializer(source='competition.teams.team', many=False)  # Связь с командой через соревнование
    score = serializers.FloatField()  # Представляем баллы как число с плавающей точкой
    created_at = serializers.DateTimeField()  # Время создания
    updated_at = serializers.DateTimeField()  # Время последнего обновления

    class Meta:
        model = Score
        fields = ['competition', 'judge_user', 'criteria', 'team', 'score', 'created_at', 'updated_at']
