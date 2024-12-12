from rest_framework import serializers

from competitions.models import Competition
from competitions.models.experiment import Experiment
from competitions.validations.Experiment import validate_experiment_register


class ExperimentSerializer(serializers.ModelSerializer):
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    competition_id = serializers.PrimaryKeyRelatedField(
        queryset=Competition.objects.all(), source='competition'
    )

    class Meta:
        model = Experiment
        fields = ['id', 'name', 'competition_id', 'competition_name']
        read_only_fields = ['id']


    def validate(self, data):
        print(data)
        validate_experiment_register(data)
        return data