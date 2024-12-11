from rest_framework import serializers
from competitions.models import Competition, CompetitionTeam
from competitions.models import Teams


class CompetitionSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Competition
    class Meta:
        model = Competition
        fields = ['name', 'description', 'created_at', 'updated_at']


class CompetitionTeamSerializer(serializers.ModelSerializer):
    # Сериализатор для модели CompetitionTeam
    competition = CompetitionSerializer()  # Вложенный сериализатор для Competition
    team = serializers.StringRelatedField()  # Просто отображаем имя команды (или можно использовать вложенный сериализатор для Teams)

    class Meta:
        model = CompetitionTeam
        fields = ['competition', 'team']
