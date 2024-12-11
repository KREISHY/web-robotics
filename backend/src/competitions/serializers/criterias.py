from rest_framework import serializers
from competitions.models import Criteria


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ['id', 'name', 'weight']
        read_only_fields = ['id']
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

    def validate_name(self, value):
        """
        Проверка уникальности поля name.
        """
        if Criteria.objects.filter(name=value).exists():
            raise serializers.ValidationError('Критерий с таким названием уже существует.')
        return value

    def validate_weight(self, value):
        """
        Проверка валидности веса (например, от 0 до 10).
        """
        if not (0 <= value <= 10):
            raise serializers.ValidationError('Вес критерия должен быть в диапазоне от 0 до 1.')
        return value

    def validate(self, data):
        """
        Общая валидация, если нужна дополнительная логика.
        """
        if data['name'].strip() == "":
            raise serializers.ValidationError({'name': 'Название критерия не может быть только пробелами.'})
        return data
