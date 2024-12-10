from django.urls import path, include
from rest_framework import routers

from users.views.auth import UserViewSet
from users.views.registration import UserRegistrationView
from users.views.token import EmailTokenConfirmationView
from users.views.reset import ResetPasswordRequestView, ResetPasswordConfrimView

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'register', UserRegistrationView, basename='register')
router.register(r'reset/password', ResetPasswordRequestView, basename='reset-password-create')
router.register(r'email', EmailTokenConfirmationView, basename='email')

router.register(r'email', EmailTokenConfirmationView, basename='email')


urlpatterns = [
]

urlpatterns += router.urls