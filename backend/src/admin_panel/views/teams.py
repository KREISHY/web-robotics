from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from competitions.models import Teams


class TeamListView(ListView):
    model = Teams
    template_name = 'admin_panel/teams_list.html'  # Указываем путь к шаблону
    context_object_name = 'teams'  # Имя переменной, в которой будет список команд


class TeamDetailView(DetailView):
    model = Teams
    context_object_name = 'team'
    template_name = 'admin_panel/team-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_status_index = next((index for index, (value, _) in enumerate(Teams.STATUS_CHOICES) if value == self.object.status), 0)

        # Фильтруем статусы, исключая те, которые идут выше текущего
        available_statuses = Teams.STATUS_CHOICES[current_status_index + 1:]

        context['status_choices'] = available_statuses  # Передаем доступные статусы в контекст
        return context

    def post(self, request, *args, **kwargs):
        team = self.get_object()
        status = request.POST.get('status')

        if status in dict(Teams.STATUS_CHOICES).keys():
            team.status = status
            team.save()

        return redirect('team-admin-detail', pk=team.pk)  # Перенаправляем на страницу с деталями команды
