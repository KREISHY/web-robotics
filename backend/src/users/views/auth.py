from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserCurrentSerializer, UserLoginSerializer


class CurrentUserViewSet(viewsets.ViewSet):
    """
    Текущий пользователь
    Если пользователь не авторизирован указывает пустые поля
    """
    serializer_class = UserCurrentSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            serializer = UserCurrentSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


        empty_user_data = {field: "" for field in UserCurrentSerializer.Meta.fields}
        return Response(empty_user_data, status=status.HTTP_200_OK)


class UserLoginViewSet(ModelViewSet):
    """
    Вход в систему
    """
    model = User
    queryset = User.objects.none
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({
                'status': 'authenticated', 'message': 'Вы уже вошли в систему'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if request.user.is_authenticated:
            return Response({
                'status': 'authenticated', 'message': 'Вы уже вошли в систему'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            return Response({'status': 'error', 'message': 'Предоставлены неверные данные'},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutViewSet(viewsets.ViewSet):
    """
    Выход из системы
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return Response(
                {'status': 'success', 'message': 'Вы успешно вышли из системы'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {'status': 'error', 'message': 'Пользователь не авторизирован или уже вышел из системы'},
            status=status.HTTP_401_UNAUTHORIZED
        )