from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from competitions.models import Criteria
from competitions.serializers import CriteriaSerializer
from users.custom_permissions import IsAuthenticatedAndIsJudgeOrOperator


class CriteriaPagination(PageNumberPagination):
    """
    Пагинация для Criteria.
    """
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100


class CriteriaViewSet(ModelViewSet):
    """
    ViewSet для модели Criteria.
    """
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer
    permission_classes = [IsAuthenticatedAndIsJudgeOrOperator]  # Чтение для всех, изменение только для авторизованных
    pagination_class = CriteriaPagination

    def get_queryset(self):
        """
        Переопределяем queryset для фильтрации по названию критерия через GET-параметры.
        """
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def perform_create(self, serializer):
        """
        Дополнительная логика при создании.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Дополнительная логика при обновлении.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Логика при удалении.
        """
        instance.delete()
