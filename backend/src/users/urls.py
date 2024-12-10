from rest_framework import routers
from users.views.registration import UserRegistrationView

router = routers.DefaultRouter()

router.register(r'register', UserRegistrationView, basename='register')

urlpatterns = router.urls

