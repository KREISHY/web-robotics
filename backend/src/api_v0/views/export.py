from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import HttpResponse
import csv
from openpyxl import Workbook
from competitions.models import Score, Experiment, Competition, Criteria, User


class ExportCSVScoresViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='by-experiment')
    def export_by_experiment(self, request, pk=None):
        """Экспорт оценок по испытанию."""
        try:
            experiment = Experiment.objects.get(pk=pk)
        except Experiment.DoesNotExist:
            return Response({'error': 'Experiment not found'}, status=404)

        scores = Score.objects.filter(experiment=experiment).order_by('-score')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="scores_experiment_{experiment.id}.csv"'
        writer = csv.writer(response, delimiter=';')

        writer.writerow(['Team', 'Judge', 'Criteria', 'Score', 'Experiment'])
        for score in scores:
            team = score.team  # Прямое обращение к объекту команды
            writer.writerow([
                team.name if team else "Unknown",  # Проверка, существует ли команда
                score.judge_user.username,
                score.criteria.name,
                round(score.score, 1),  # Округление до одной десятичной
                score.experiment.name,
            ])
        return response

    @action(detail=True, methods=['get'], url_path='by-team')
    def export_by_team(self, request, pk=None):
        """Экспорт оценок по команде в CSV."""
        try:
            competition = Competition.objects.get(pk=pk)
        except Competition.DoesNotExist:
            return Response({'error': 'Competition not found'}, status=404)

        scores = Score.objects.filter(competition=competition)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="scores_team_{competition.id}.csv"'
        writer = csv.writer(response, delimiter=';')

        writer.writerow(['Experiment', 'Judge', 'Criteria', 'Score', 'Team'])
        for score in scores:
            team_name = score.experiment.competition.teams.filter(
                pk=competition.id).first().name if score.experiment.competition.teams.exists() else "Unknown"
            writer.writerow([
                score.experiment.name,
                score.judge_user.username,
                score.criteria.name,
                round(score.score, 1),
                team_name,
            ])

        return response