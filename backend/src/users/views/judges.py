from rest_framework import viewsets, permissions

from users.models import User
from users.serializers import UserCurrentSerializer


class JudgeViewSet(viewsets.ModelViewSet):
    serializer_class = UserCurrentSerializer  # Укажите ваш сериализатор для модели пользователя
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фильтруем пользователей с использованием метода is_judge
        return User.objects.all().filter(id__in=[
            user.id for user in User.objects.all() if user.is_judge()
        ])


class OperatorViewSet(viewsets.ModelViewSet):
    serializer_class = UserCurrentSerializer  # Укажите ваш сериализатор для модели пользователя
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фильтруем пользователей с использованием метода is_judge
        return User.objects.all().filter(id__in=[
            user.id for user in User.objects.all() if user.is_operator()
        ])