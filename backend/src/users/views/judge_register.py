from django.contrib.auth.models import Group
from django.http import FileResponse
from rest_framework import viewsets, status, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from competitions.models import CompetitionJudges, Competition
from competitions.serializers import CompetitionJudgesSerializer
from users.custom_permissions import IsAuthenticatedAndIsOperator
from users.models import User
from users.serializers import JudgeRegisterSerializer


class JudgeRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = JudgeRegisterSerializer
    permission_classes = [IsAuthenticatedAndIsOperator]
    http_method_names = ['get', 'post', 'head', 'options', 'list']

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user, user_data = serializer.save()

            # Находим или создаем группу "Judges"
            judges_group, created = Group.objects.get_or_create(name='Judges')

            # Добавляем пользователя в группу
            user.groups.add(judges_group)

            return Response({
                "message": f"Пользователь {user.username} был успешно создан и добавлен в группу 'Judges'.",
                "email": user.email,
                "username": user.username,
                "password": user_data['password'],
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompetitionJudgesViewSet(viewsets.ModelViewSet):
    queryset = CompetitionJudges.objects.all()
    serializer_class = CompetitionJudgesSerializer

    def create(self, request, *args, **kwargs):
        # Получаем id судьи и соревнования из запроса
        judge_id = request.data.get('judge')
        competition_id = int(request.data.get('competition'))

        if not judge_id or not competition_id:
            return Response({"detail": "Необходимо предоставить ID судьи и соревнования."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли судья и соревнование
        judge = get_object_or_404(User, id=judge_id)
        competition = get_object_or_404(Competition, id=competition_id)

        # Создаем данные для сериализатора
        data = {
            'judge': judge.id,  # передаем ID судьи
            'competition': competition.id  # передаем ID соревнования
        }

        # Используем сериализатор для валидации данных
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            # Если данные валидны, сохраняем объект в базу
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        # Получаем объект для удаления
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        # Удаляем объект
        instance.delete()
