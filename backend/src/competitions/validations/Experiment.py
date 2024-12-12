from rest_framework import serializers

from competitions.models import Competition


def validate_experiment_register(data):
    competition = data.get('competition')

    if not competition:
        raise serializers.ValidationError({'competition_id': 'Пожалуйста, введите соревнование.'})

    return data
