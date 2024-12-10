from rest_framework import routers

from config import URL_EMAIL_VERIFY, URL_PASSWORD_RESET_VERIFY
from users.views.auth import CurrentUserViewSet, UserLoginViewSet, UserLogoutViewSet
from users.views.registration import UserRegistrationView
from users.views.email_confirm_token import EmailTokenConfirmationView
from users.views.reset import ResetPasswordRequestView, ResetPasswordConfirmationView

"URL для подтверждения почты из файла конфига"
email_verify_url = URL_EMAIL_VERIFY.replace("/", "")
password_reset_confirm_url = URL_PASSWORD_RESET_VERIFY.replace("/", "")

router = routers.DefaultRouter()
router.register(r'current-user', CurrentUserViewSet, basename='current-user')
router.register(r'login', UserLoginViewSet, basename='login')
router.register(r'logout', UserLogoutViewSet, basename='logout')
router.register(r'register', UserRegistrationView, basename='register')
router.register(email_verify_url, EmailTokenConfirmationView, basename=email_verify_url)
router.register(r'password-reset-create', ResetPasswordRequestView, basename='password-reset-create')
router.register(password_reset_confirm_url, ResetPasswordConfirmationView, basename=password_reset_confirm_url)



urlpatterns = [
]

urlpatterns += router.urls