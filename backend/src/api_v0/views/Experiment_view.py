from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from competitions.models.experiment import Experiment
from competitions.serializers.experiment import ExperimentSerializer


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'head']
    permission_classes = [IsAuthenticatedOrReadOnly]
