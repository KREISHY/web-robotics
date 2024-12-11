from rest_framework import serializers
from competitions.models import Competition
from competitions.models import Teams


class CompetitionSerializer(serializers.ModelSerializer):
    # Сериализатор для модели Competition
    class Meta:
        model = Competition
        fields = ['name', 'description', 'created_at', 'updated_at']

