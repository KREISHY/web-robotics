from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import UserCurrentSerializer, UserLoginSerializer


class UserViewSet(viewsets.ViewSet):
    """
    UserViewSet предоставляет два действия:
    - Вход пользователя (login)
    - Выход пользователя (logout)
    """
    serializer_class = UserCurrentSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        """
        Возвращает информацию о текущем пользователе.
        Если пользователь не аутентифицирован, возвращает сериализованные пустые данные.
        """
        user = request.user

        if user.is_authenticated:
            serializer = UserCurrentSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Создаем пустой объект для возврата структуры сериализатора с пустыми значениями
            empty_user_data = {field: "" for field in UserCurrentSerializer.Meta.fields}
            return Response(empty_user_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='login', permission_classes=[permissions.AllowAny], serializer_class=UserLoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return Response({'status': 'success', 'message': 'Вы успешно вошли в систему'}, status=status.HTTP_200_OK)
            return Response({'status': 'error', 'message': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], url_path='logout', permission_classes=[permissions.IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        try:
            logout(request)
            return Response({'status': 'success', 'message': 'Вы успешно вышли из системы'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'error', 'message': 'Произошла ошибка при выходе'}, status=status.HTTP_400_BAD_REQUEST)