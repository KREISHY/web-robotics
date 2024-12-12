from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from competitions.models import Score
from competitions.serializers.score import ScoreSerializer


class ScoreViewSet(ModelViewSet):
    """
    ViewSet для управления баллами.
    """
    queryset = Score.objects.all().select_related('competition', 'judge_user', 'criteria', 'experiment')
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter]
    filterset_fields = ['competition', 'judge_user', 'criteria', 'experiment']
    ordering_fields = ['score', 'created_at', 'updated_at']
    search_fields = ['competition__name', 'judge_user__username', 'criteria__name', 'experiment__name']

    def perform_create(self, serializer):
        """
        Дополнительная логика при создании объекта.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Дополнительная логика при обновлении объекта.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Дополнительная логика при удалении объекта.
        """
        instance.delete()
