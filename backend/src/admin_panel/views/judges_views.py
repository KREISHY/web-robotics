from django.db.models import Case, When, Value, BooleanField
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from competitions.models import Competition
from users.models import User


class JudgesListView(ListView):
    model = User
    context_object_name = 'judges'
    template_name = 'admin_panel/judges_list.html'

    def get_queryset(self):
        queryset = User.objects.annotate(
            is_judge_status=Case(
                When(groups__name='Operators', then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).filter(is_judge_status=True)
        return queryset


class JudgeDetailView(DetailView):
    model = User
    context_object_name = 'judge'
    template_name = 'admin_panel/judges_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем судью
        judge = self.get_object()

        # Получаем все соревнования, в которых судья еще не участвует
        competitions = Competition.objects.exclude(
            competitionjudges__judge=judge
        )

        # Добавляем в контекст список соревнований, в которых судья не участвует
        context['competitions'] = competitions

        # Получаем уже назначенные соревнования для этого судьи
        assigned_competitions = judge.competitionjudges_set.all()

        # Добавляем в контекст уже назначенные соревнования
        context['assigned_competitions'] = assigned_competitions

        return context


class CreateJudgeView(View):
    def get(self, request):
        # Рендерим страницу с формой создания судьи
        return render(request, 'admin_panel/judge_create.html')