from django.contrib import admin

from api_v0.views.Experiment_view import ExperimentViewSet
from .models import Competition, Criteria, Log, Score, Teams
from .models.experiment import Experiment


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'start_registration', 'end_registration')
    list_filter = ('created_at', 'start_registration', 'end_registration')
    search_fields = ('name', )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)  # Сортировка по дате добавления (от новых к старым)


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')
    list_filter = ('weight',)
    search_fields = ('name',)
    ordering = ('-weight',)  # Сортировка по убыванию веса


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'action')
    list_filter = ('timestamp', 'user__username')
    search_fields = ('user__username', 'action')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)  # Сортировка по времени изменений


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('competition', 'judge_user', 'criteria', 'score', 'created_at')
    list_filter = ('competition__name', 'judge_user__username', 'criteria__name')
    search_fields = ('competition__name', 'judge_user__username', 'criteria__name')
    date_hierarchy = 'created_at'
    ordering = ('-score',)  # Сортировка по убыванию баллов


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'institution', 'leader', 'status')
    list_filter = ('city', 'status', 'leader')
    search_fields = ('name', 'city', 'institution', 'leader')
    list_editable = ('status',)
    list_per_page = 20
    ordering = ('name',)  # Сортировка по алфавиту


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('name', 'competition')  # Отображаемые поля в списке
    list_filter = ('competition__name',)  # Фильтр по названию соревнования
    search_fields = ('name', 'competition__name')  # Поля для поиска
    list_per_page = 20  # Количество элементов на страницу
    ordering = ('name',)  # Сортировка по имени