from rest_framework import serializers
from competitions.models import Criteria


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ['name', 'weight']  # Указываем поля, которые должны быть в сериализаторе
