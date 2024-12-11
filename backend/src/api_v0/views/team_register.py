from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from competitions.models import Teams, Competition
from competitions.serializers.team import TeamRegisterSerializer, TeamSSerializer


class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamSSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]


class TeamRegisterViewSet(viewsets.ModelViewSet):
    """
    "name": "Название команды (строка, обязательно, макс. 255 символов)",
    "robot_name": "Название робота (строка, обязательно, макс. 255 символов)",
    "city": "Название города (строка, обязательно, макс. 255 символов)",
    "institution": "Учебное заведение (строка, обязательно, макс. 255 символов)",
    "members": "Члены команды (строка, необязательно)",
    "leader": "Руководитель команды (строка, необязательно, по умолчанию капитан команды)",
    "contact_phone": "Телефон (строка, обязательно, начинается с +7 или 8)",
    "comments": "Комментарий (строка, необязательно)",
    "competition": "ID соревнования (число, обязательно, должно существовать)"
    """
    queryset = Teams.objects.none
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    serializer_class = TeamRegisterSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(Teams.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)