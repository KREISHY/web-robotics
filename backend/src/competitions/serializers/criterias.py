from rest_framework import serializers
from competitions.models import Criteria, Competition


class CriteriaSerializer(serializers.ModelSerializer):
    competition_name = serializers.CharField(source='competitions.name', read_only=True)
    competition = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all(), write_only=True)

    class Meta:
        model = Criteria
        fields = ['id', 'name', 'weight', 'competition', 'competition_name']
        read_only_fields = ['id', 'competition_name']
        extra_kwargs = {
            'name': {
                'required': True,
                'error_messages': {
                    'required': 'Название критерия обязательно для заполнения.',
                    'blank': 'Название критерия не может быть пустым.'
                }
            },
            'weight': {
                'required': True,
                'error_messages': {
                    'required': 'Вес критерия обязателен для заполнения.',
                    'invalid': 'Вес критерия должен быть числом.'
                }
            }
        }

    def create(self, validated_data):
        """
        Обработка создания объекта Criteria.
        """
        competition = validated_data.pop('competition')  # Извлекаем Competition из данных
        criteria = Criteria.objects.create(competitions=competition, **validated_data)
        return criteria
