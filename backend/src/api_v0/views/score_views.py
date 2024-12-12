from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from competitions.models import Score
from competitions.serializers.score import ScoreSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class ScoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления баллами.
    """
    queryset = Score.objects.all().select_related('competition', 'judge_user', 'criteria', 'experiment')
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['score', 'created_at', 'updated_at']
    search_fields = ['competition__name', 'competition__id', 'judge_user__username', 'criteria__name', 'experiment__name']

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

    def get_queryset(self):
        """
        Фильтрация по `competition_id` если передан параметр `competition_id`.
        """
        queryset = self.queryset

        competition_id = self.request.query_params.get('competition_id', None)
        if competition_id is not None:
            queryset = queryset.filter(competition__id=competition_id)

        return queryset

    @action(detail=False, methods=['get'])
    def filter_by_competition_id(self, request):
        """
        Пользовательский фильтр для поиска по `competition_id`.
        """
        competition_id = request.query_params.get('competition_id', None)
        if competition_id is not None:
            queryset = Score.objects.filter(competition__id=competition_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"detail": "competition_id parameter is required"}, status=400)
