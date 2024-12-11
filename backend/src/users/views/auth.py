from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserCurrentSerializer, UserLoginByEmailSerializer, UserLoginByUsernameSerializer


class CurrentUserViewSet(viewsets.ViewSet):
    """
    Текущий пользователь
    Если пользователь не авторизирован указывает пустые поля
    """
    serializer_class = UserCurrentSerializer
    http_method_names = ['get', 'post' ,'head', 'options', 'list']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user

        serializer = UserCurrentSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginByEmailViewSet(ModelViewSet):
    """
    Вход в систему
    """
    model = User
    queryset = User.objects.none
    serializer_class = UserLoginByEmailSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post' ,'head', 'options', 'list']

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


class LoginByUsernameViewSet(ModelViewSet):
    """
    Вход в систему
    """
    model = User
    queryset = User.objects.none
    serializer_class = UserLoginByUsernameSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post' ,'head', 'options', 'list']

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
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            try:
                email = User.objects.get(username=username).email
            except User.DoesNotExist:
                raise serializers.ValidationError({'username': 'Пользователь с таким именем не найден.'})

            if not email:
                raise serializers.ValidationError({'username': 'Ошибка, у пользователя отсутствует почта. '
                                                               'Обратитесь в техническую поддержку.'})

            user = authenticate(request, email=email, password=password)
            if user:
                # Проверка ролей пользователя
                if not (user.is_superuser or user.is_judge() or user.is_operator or user.is_staff):
                    raise serializers.ValidationError({'username': 'Вход запрещён. У вас нет прав доступа.'})

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
    http_method_names = ['get', 'post' ,'head', 'options', 'list']

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