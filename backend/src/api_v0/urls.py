from rest_framework.routers import DefaultRouter
from api_v0.views.team_register import TeamRegisterViewSet, TeamsViewSet

router = DefaultRouter()

router.register(r'team-register', TeamRegisterViewSet, basename='team-register')
router.register(r'teams', TeamsViewSet, basename='teams')


urlpatterns = [

]

urlpatterns += router.urls