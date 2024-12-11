from rest_framework import serializers
from competitions.models import Score, Competition, Criteria, Experiment
from users.models import User


class ScoreSerializer(serializers.ModelSerializer):
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    criteria_name = serializers.CharField(source='criteria.name', read_only=True)
    judge_name = serializers.CharField(source='judge_user.username', read_only=True)
    experiment_name = serializers.CharField(source='experiment.name', read_only=True)

    competition = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all(), write_only=True)
    judge_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    criteria = serializers.PrimaryKeyRelatedField(queryset=Criteria.objects.all(), write_only=True)
    experiment = serializers.PrimaryKeyRelatedField(queryset=Experiment.objects.all(), write_only=True)

    class Meta:
        model = Score
        fields = [
            'id', 'competition', 'competition_name',
            'judge_user', 'judge_name',
            'criteria', 'criteria_name',
            'experiment', 'experiment_name',
            'score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'competition_name', 'judge_name', 'criteria_name', 'experiment_name', 'created_at', 'updated_at']
        extra_kwargs = {
            'score': {
                'required': True,
                'error_messages': {
                    'required': 'Поле "баллы" обязательно для заполнения.',
                    'invalid': 'Баллы должны быть числом от 0 до 100.',
                }
            }
        }

    def validate_score(self, value):
        """
        Валидация поля score (например, проверка диапазона).
        """
        if not (0.0 <= value <= 100.0):
            raise serializers.ValidationError('Баллы должны быть в диапазоне от 0 до 100.')
        return value

    def validate(self, data):
        """
        Общая валидация, например, проверка уникальности судьи, критерия и эксперимента в рамках соревнования.
        """
        competition = data.get('competition')
        judge_user = data.get('judge_user')
        criteria = data.get('criteria')
        experiment = data.get('experiment')

        if Score.objects.filter(
            competition=competition,
            judge_user=judge_user,
            criteria=criteria,
            experiment=experiment
        ).exists():
            raise serializers.ValidationError(
                'Судья уже оценил это испытание по данному критерию в рамках соревнования.'
            )
        return data

    def create(self, validated_data):
        """
        Создание объекта Score с поддержкой обработанных полей.
        """
        return Score.objects.create(**validated_data)
