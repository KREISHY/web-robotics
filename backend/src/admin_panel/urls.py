from django.urls import path

from admin_panel.views.admin_login import admin_login
from admin_panel.views.admin_main import admin_main
from admin_panel.views.judges_views import JudgesListView, JudgeDetailView, CreateJudgeView
from admin_panel.views.teams import TeamListView, TeamDetailView

urlpatterns = [
    path('', admin_main, name='index'),
    path('login/', admin_login, name='admin-login'),
    path('judges-list/', JudgesListView.as_view(), name='judges-admin-list'),
    path("judge-detail/<pk>", JudgeDetailView.as_view(), name='judge-admin-detail'),
    path('judge-create/', CreateJudgeView.as_view(), name='judge-admin-create'),
    path('teams-list/', TeamListView.as_view(), name='teams-admin-list'),
    path('team-detail/<pk>', TeamDetailView.as_view(), name='team-admin-detail'),
]

