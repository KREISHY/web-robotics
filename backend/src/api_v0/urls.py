from rest_framework import routers

from api_v0.views.competitions import CompetitionViewSet
from api_v0.views.team_register import TeamRegisterViewSet, TeamsViewSet

router = routers.DefaultRouter()
router.register(r'competition', CompetitionViewSet, basename='competition')


router.register(r'team-register', TeamRegisterViewSet, basename='team-register')
router.register(r'teams', TeamsViewSet, basename='teams')

urlpatterns = [

]

urlpatterns += router.urls