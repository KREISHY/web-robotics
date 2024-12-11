from rest_framework import routers

from api_v0.views.competitions import CompetitionViewSet

router = routers.DefaultRouter()
router.register(r'competition', CompetitionViewSet, basename='competition')


urlpatterns = [

]
urlpatterns += router.urls