from rest_framework import routers

from api_v0.views.Experiment_view import ExperimentViewSet
from api_v0.views.competitions import CompetitionViewSet
from api_v0.views.team_register import TeamRegisterViewSet, TeamsViewSet
from api_v0.views.criteria import CriteriaViewSet

router = routers.DefaultRouter()
router.register(r'competition', CompetitionViewSet, basename='competition')


router.register(r'team-register', TeamRegisterViewSet, basename='team-register')
router.register(r'teams', TeamsViewSet, basename='teams')
router.register(r'criteria', CriteriaViewSet, basename='criteria')
router.register(r'experiment', ExperimentViewSet, basename='experiment')


urlpatterns = [

]

urlpatterns += router.urls