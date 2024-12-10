from django.urls import path
from admin_panel.views.admin_main import admin_main

urlpatterns = [
    path('', admin_main, name='admin_main')
]

