# views.py
from django.views.generic import ListView, DetailView
from competitions.models.competitions import Competition

class CompetitionListView(ListView):
    model = Competition
    template_name = 'admin_panel/competitions_list.html'
    context_object_name = 'competitions'
    queryset = Competition.objects.all().order_by('-created_at')


class CompetitionDetailView(DetailView):
    model = Competition
    template_name = 'admin_panel/competition_detail.html'
    context_object_name = 'competition'