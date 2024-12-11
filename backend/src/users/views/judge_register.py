from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from users.custom_permissions import IsAuthenticatedAndIsOperator
from users.models import User
from users.serializers import JudgeRegisterSerializer


class JudgeRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none
    serializer_class = JudgeRegisterSerializer
    permission_classes = [IsAuthenticatedAndIsOperator]
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
