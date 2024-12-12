from rest_framework import serializers

from rest_framework import serializers
import re

from competitions.models import Competition, Teams


def validate_team_register(data, user):
    contact_phone = data.get('contact_phone')
    if contact_phone:
        if contact_phone.startswith('+7'):
            if len(contact_phone) != 12:
                raise serializers.ValidationError({'contact_phone': 'Пожалуйста, введите корректный номер телефона.'})
        elif contact_phone.startswith('8'):
            if len(contact_phone) != 11:
                raise serializers.ValidationError({'contact_phone': 'Пожалуйста, введите корректный номер телефона.'})
        else:
            raise serializers.ValidationError({'contact_phone': 'Номер телефона должен начинаться с +7 или 8.'})

    # Проверка существования соревнования с указанным id
    competition = data.get('competition')
    if competition and not Competition.objects.filter(id=competition.id).exists():
        raise serializers.ValidationError({'competition': 'Соревнование не найдено.'})

    if not Competition.objects.first(id=competition.id).registrations_is_running:
        raise serializers.ValidationError({'competition': 'Регистрация на соревнование окончена или ещё не началась.'})

    if Teams.objects.filter(captain=user, competition=competition).exists():
        raise serializers.ValidationError({'competition': 'Вы уже зарегистрировались на это соревнование.'})


    return data