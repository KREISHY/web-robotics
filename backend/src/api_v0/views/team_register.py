from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from competitions.models import Teams, Competition
from competitions.serializers.team import TeamRegisterSerializer, TeamSSerializer


class TeamsViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head', 'options', 'head', 'list']

    def get_queryset(self):
        competition_id = self.request.query_params.get('competition_id')

        if competition_id is not None:
            try:
                queryset = Teams.objects.filter(competition_id=competition_id)
                if not queryset.exists():
                    raise NotFound('No teams found for the provided competition_id.')
                return queryset
            except ValueError:
                raise NotFound('Invalid competition_id provided.')
        return Teams.objects.all()



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