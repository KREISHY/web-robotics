from django.utils.timezone import now
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from competitions.models import Competition, CompetitionTeam
from competitions.serializers.competition import CompetitionSerializer, CompetitionTeamSerializer


class CompetitionViewSet(ModelViewSet):
    """
    ViewSet для модели Competition.
    """
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Чтение для всех, изменение только для авторизованных

    def get_queryset(self):
        """
        Переопределяем метод для фильтрации записей:
        - По умолчанию возвращаются записи, где текущая дата между start_registration и end_registration.
        - Суперпользователь может запросить все записи с параметром ?all=true.
        """
        queryset = Competition.objects.all()
        user = self.request.user

        if not (user.is_superuser and self.request.query_params.get('all') == 'true'):
            current_time = now()
            queryset = queryset.filter(
                start_registration__lte=current_time,
                end_registration__gte=current_time
            )

        # Фильтр по названию соревнования (опционально).
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_permissions(self):
        """
        Переопределяем разрешения:
        - Для списка и просмотра записей доступ открыт для всех.
        - Для создания, изменения и удаления требуется суперпользователь.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


class CompetitionTeamViewSet(ModelViewSet):
    """
    ViewSet для модели CompetitionTeam.
    """
    queryset = CompetitionTeam.objects.select_related('competition', 'team')  # Оптимизация запросов
    serializer_class = CompetitionTeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Фильтрация по соревнованию или команде через GET-параметры.
        """
        queryset = super().get_queryset()
        competition_id = self.request.query_params.get('competition', None)
        team_id = self.request.query_params.get('team', None)
        if competition_id:
            queryset = queryset.filter(competition_id=competition_id)
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        return queryset
