from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from users.custom_permissions import IsAuthenticatedAndIsSuperuser
from users.models import User
from users.serializers import OperatorRegisterSerializer


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none
    serializer_class = OperatorRegisterSerializer
    permission_classes = [IsAuthenticatedAndIsSuperuser]
    http_method_names = ['get', 'post' ,'head', 'options', 'list']

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user, user_data = serializer.save()
            return Response({
                "message": f"Пользователь {user.username} был успешно создан.",
                "email": user.email,
                "username": user.username,
                "password": user_data['password'],
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)